FROM python:3.5
MAINTAINER Ville Koivunen <ville.koivunen@hel.fi>
# This image cleans up after itself on apt-get calls
RUN apt-get update && apt-get install -y libgdal1h postgresql-client-9.4
RUN mkdir /code && mkdir -p /srv/files && mkdir /srv/config
COPY . /code/
WORKDIR /code
RUN mv Docker/apiserver/docker-django-settings.py local_settings.py && \
    mv Docker/apiserver/docker-entrypoint.sh docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh
RUN pip install -r requirements.txt && pip install uwsgi
# /srv/files must be writable by the application user as staticfiles
# are deposited there, and that only be done after the final
# configuration files are available during runtime
RUN adduser --system respa && chown respa /srv/files
USER respa
VOLUME /srv/config
CMD /code/docker-entrypoint.sh
