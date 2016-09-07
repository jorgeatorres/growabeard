# encoding: utf-8

import dj_database_url

from growabeard.settings.default import *

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# https://devcenter.heroku.com/articles/django-app-configuration#database-configuration
DATABASES = {
    'default': dj_database_url.config()
}
