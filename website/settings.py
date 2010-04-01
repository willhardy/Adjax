# Django settings for adjax website.

import os
PROJECT_DIR = os.path.dirname(__file__)
project_dir = lambda p: os.path.join(PROJECT_DIR, p)


DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ( ('Will Hardy', 'adjax@hardysoftware.com.au'),)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': project_dir('test.db'),                      # Or path to database file if using sqlite3.
    }
}

TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'en-us'
USE_I18N = False


MEDIA_ROOT = project_dir('media')
MEDIA_URL = '/media/'
# This needs to be set otherwise it conflicts with MEDIA_URL
ADMIN_MEDIA_PREFIX = '/media/admin/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (project_dir('templates'),)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'website.urls'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'adjax', 
    'basic'
    )
