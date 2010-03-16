# Django settings for adjax website.

import os
PROJECT_DIR = os.path.dirname(__file__)
project_dir = lambda p: os.path.join(PROJECT_DIR, p)


DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ( ('Will Hardy', 'adjax@hardysoftware.com.au'),)
MANAGERS = ADMINS


TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'en-us'
USE_I18N = False


MEDIA_ROOT = project_dir('media')
MEDIA_URL = '/media/'
# This needs to be set otherwise it conflicts with MEDIA_URL
ADMIN_MEDIA_PREFIX = '/media/admin/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)
TEMPLATE_DIRS = (project_dir('templates'),)


MIDDLEWARE_CLASSES = (
)


ROOT_URLCONF = 'website.urls'
INSTALLED_APPS = ()
