from .base import *


# secret key 보호를 위한 작업
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = read_secret("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'poppymail_db',
        'USER': 'root',
        'PASSWORD': read_secret("MYSQL_PASSWORD"),
        'HOST': 'mariadb',
        'PORT': '3306',
    }
}

SIMPLE_JWT = {
    'SIGNING_KEY': SECRET_KEY,
}

# E-mail related settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'poppymail1234@gmail.com'
EMAIL_HOST_PASSWORD = read_secret("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = 'poppymail1234@gmail.com'
DEFAULT_FROM_MAIL = 'POPPYMAIL 관리자'

TEAM_PW = read_secret('TEAM_PW')