# This is the secure settings file, which is not tracked through git
# This is a development-mode sample; all values must be updated in production


SECRET_KEY = 'phm=9oy0g*dn!e_5_gz^*anehn)w(5x$d-3e0_-$pec6xcy2_x'

DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}