# encoding: utf-8

import os

GROWABEARD_ENVIRONMENT = os.environ.get('GROWABEARD_ENVIRONMENT', 'development')

if GROWABEARD_ENVIRONMENT == 'development':
    from growabeard.settings.development import *
else:
    from growabeard.settings.production import *
