#!/bin/bash
# We want to exit if any step fails
set -e
set -u
# Flag to keep errors that are handled
error_state=0

TIMESTAMP_FORMAT="+%Y-%m-%d %H:%M:%S"
function _log () {
    echo $(date "$TIMESTAMP_FORMAT"): $@
}

_log "Ensuring HSTORE extensions are available"
psql -h $DATABASE_HOST -U $DATABASE_USER -c "CREATE EXTENSION IF NOT EXISTS hstore;" || error_state=$?
if [ $error_state -ne 0 ]; then
  _log "Creating extension failed. Assuming database connectivity is lost. Sleeping 10s"
  sleep 10
  _log "Exiting to allow orchestration to retry"
  exit 1
fi
_log "Doing migrations (in $HOME)"
cd $HOME/respa
../venv/bin/python manage.py migrate || error_state=$?
if [ $error_state -ne 0 ]; then
  _log "Migrations failed. Assuming database connectivity is lost. Sleeping 10s"
  sleep 10
  _log "Exiting to allow orchestration to retry"
  exit 1
fi
_log "Collecting static files"
../venv/bin/python manage.py collectstatic --no-input
_log "Starting uwsgi"
uwsgi --yml /etc/uwsgi/apps-available/respa-api.yml
