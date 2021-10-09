from .base import *

# secret key 보호를 위한 작업
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# reading .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'poppymail_db',  # 데이터베이스 명
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '3306'
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
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = 'poppymail1234@gmail.com'
DEFAULT_FROM_MAIL = 'poppymail1234'

TEAM_PW = env('TEAM_PW')
