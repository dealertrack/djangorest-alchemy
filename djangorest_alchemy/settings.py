ROOT_URLCONF = 'djangorest_alchemy.tests.test_viewsets'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
        'USER': '',
        'HOST': '',
        'PORT': '',
    }
}

SECRET_KEY = "4k^rs)v0h5&8l2wiiko0x1^1ss!9fbur8_q%lb60gc&4&l!)us"
ALLOWED_HOSTS = '*'
