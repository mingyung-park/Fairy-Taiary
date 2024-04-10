"""
Django settings for fairy_tairy project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from storages.backends.s3boto3 import S3Boto3Storage
import datetime
import environ
from pathlib import Path
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# Dj-Rest-Auth See: https://dj-rest-auth.readthedocs.io/en/latest/installation.html
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
OPENAI_API_KEY = env('OPENAI_API_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'diaries',
    'emotion_chat',
    'images',
    'books',
    'recommend_music',
    'users',
    'community',
    
    #default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #DRF
    'rest_framework',
    
    #DRF Authentication
    'rest_framework.authtoken',
    # 'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django.contrib.sites',
    
    #Django Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    #s3
    'storages',
    
    #drf_yasg
    'drf_yasg',
    
    # crispy for filtering, search, sort
    # 'crispy_forms',
    
    # 단위 테스트 django-node
    # 'django-nose',
]


#Site설정
SITE_ID = 1

#dj-rest-auth
USE_JWT = True
ACCOUNT_USERNAME_REQUIRED = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False 

# 회원가입 과정에서 이메일 인증 사용 X
ACCOUNT_EMAIL_VERIFICATION = 'none' 


# REST framework 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        # "rest_framework.authentication.SessionAuthentication",
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_FILTER_BACKENDS':[
    #     'rest_framework.filters.DjangoFilterBackend',
    #     'rest_framework.filters.SearchFilter',
    #     'rest_framework.filters.OrderingFilter',
    # ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
    
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    
    # want refresh token
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    # set refresh token http only (security essue)
    'JWT_AUTH_HTTPONLY': False,
    # JWT 쿠키 csrf 검사
    'JWT_AUTH_COOKIE_USE_CSRF' : True,
    # set Session login false : if true, sessionid remains in cookie info
    'SESSION_LOGIN' : False
}
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    # JWT 토큰의 유효기간 설정
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # JWT 토큰 갱신의 유효기간
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.TokenAuthentication',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'fairy_tairy.urls'

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fairy_tairy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PW'),
        'HOST': env('DB_HOST'), 
        'PORT': env('DB_PORT'),    
        'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'",
    }
}



## AWS S3 Setting
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID =env('S3_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME =  env('S3_THREEPARK_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME =env('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024000000 # value in bytes 1GB here
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024000000

# storage URL Setting


# DEFAULT_FILE_STORAGE = 'fairy_tairy.storages.S3DefaultStorage'
MEDIA_URL = "http://%s/media/" % AWS_S3_CUSTOM_DOMAIN
STATIC_URL ="http://%s/static/" % AWS_S3_CUSTOM_DOMAIN
'''


'''

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
