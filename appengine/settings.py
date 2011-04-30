# Initial settings.py for a Kiwi project - this file is not copyrighted.

# In general, you will not change this file.

# Instead, customize Kiwi through kiwisettings.py in your root directory
# You can copy kiwisettings.py from the kiwi directory or start with a blank
# file and only specify those options you wish to change.


import os

# When Django emails errors, it uses these lists.
# ADMINS get notifications of errors; MANAGERS get notifications of broken links
ADMINS = (
    ('Name', 'email@email.email'),
)
MANAGERS = ADMINS
    
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'PST8PDT US'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media. Example: "/home/media/media.lawrence.com/"
# URL that handles the media served from MEDIA_ROOT. Example: "http://media.lawrence.com"
MEDIA_ROOT = ''
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Only needed if you use the security hash feature of Django'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'kiwi.middleware.KiwiMiddleware',                                   # KIWI BOGUS - Can this be auto-installed?
    # 'django.contrib.sessions.middleware.SessionMiddleware',           # Doesn't apply to Google App Engine
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # "django.core.context_processors.auth",           # Doesn't apply to Google App Engine
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "kiwi.middleware.context_processor",               # BOGUS KIWI INSTALL: Auto-install?
    )


ROOT_URLCONF = 'urls'

import os.path
dirHome = os.path.dirname(__file__)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(dirHome, 'templates').replace('\\', '/'),
    dirHome.replace('\\', '/')          # BOGUS: KIWI - Should I do this differently?
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
    'django.contrib.sites',
)
