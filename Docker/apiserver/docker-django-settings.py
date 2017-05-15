# Ansible managed: /Users/ville/Documents/helsinki-deployment/roles/django-configuration/templates/django_local_settings.py.j2 modified on 2016-12-06 19:07:19 by ville on Omena.local
# Read in a fragment directory. Easier than trying to splice them
# all over the template
import os
local_settings_d = '/srv/django_local_settings.d'
if os.path.isdir(local_settings_d):
    for file in sorted(os.listdir(local_settings_d)):
        if not file.endswith('.py'):
            continue
        exec(open(os.path.join(local_settings_d, file), "rb").read())
