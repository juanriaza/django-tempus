from __future__ import unicode_literals

CACHES = {
    'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'tempus'
)

ROOT_URLCONF = 'tempus.tests.urls'

SECRET_KEY = 'tempusfugit'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'tempus.contrib.auto_login.middleware.AutoLoginMiddleware',
    'tempus.tests.utils.PromoMiddleware'
)
