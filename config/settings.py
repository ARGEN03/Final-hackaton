"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split()


# Application definition

DJANGO_APPS = [
    'jazzmin',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ADDITIONAL_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'django_filters',
    'corsheaders',
]

OWN_APPS = [
    'account',
    'genre',
    'movie',
    'plan',
    'favorite',
    'comment',
    'rating',
    'viewed',
]

INSTALLED_APPS = ADDITIONAL_APPS + OWN_APPS + DJANGO_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{message}\n',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': 'information.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],  # Добавьте обработчик 'file' для журналирования в файл
        },
        'django.request': {
            'handlers': ['console', 'file'],  # Добавьте обработчик 'file' для журналирования в файл
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

AUTH_USER_MODEL = 'account.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

REDIS_HOST = 'redis'
REDIS_PORT = '6379'

CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=90),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
#         "LOCATION": os.path.join(BASE_DIR, "config_cache"),
#     }
# }
# JAZZMIN_UI_TWEAKS = {  
#     "theme": "darkly",  
#     "sticky_actions": True,  
#     "actions_sticky_top": True,  
# }  

# JAZZMIN_SETTINGS = {
#     "site_title": " My favorite movie AdminPanel",
#     "site_header": "My favorite movie",
#     "site_logo": "images/logo.png",  # Путь к вашему логотипу
#     "site_logo_classes": "img-circle",
#     "welcome_sign": "Добро пожаловать в My favorite movi",
#     "show_sidebar": True,
#     "navigation_expanded": True,
#     "hide_apps": ["social_django", "auth"],
#     "usermenu_links": [
#         {
#             "name": "Помощь",
#             "url": "https://www.google.com/",
#             "new_window": True
#         },
#         {
#             "model": "auth.user"
#         }
#     ],
#     "topmenu_links": [
#         # Ссылки, отображаемые в верхнем меню
#         {"name": "Домой", "url": "admin:index",
#          "permissions": ["auth.view_user"]},
#         {"name": "Поддержка", "url": "https://www.google.com/",
#          "new_window": True},
#     ],
#     "show_ui_builder": True,
#     "changeform_format": "horizontal_tabs",
#     # Используйте горизонтальные вкладки на страницах редактирования
#     "changeform_format_overrides": {"auth.user": "collapsible",
#                                     "auth.group": "vertical_tabs"},
#     "show_icons": True,  # Показывать иконки в меню
#     "default_theme": "cerulean",  # Используйте тему Cerulean из Bootswatch
#     "related_modal_active": True,
#     # Включить модальные окна для связанных объектов
# }

JAZZMIN_UI_TWEAKS = {  
    "theme": "solar",  # Устанавливаем тему Flatly
    "sticky_actions": True,  # Включаем закрепленные действия
    "actions_sticky_top": True,  # Закрепляем действия вверху
} 

JAZZMIN_SETTINGS = {
    "site_brand": "Admin",  # Название сайта
    "welcome_sign": "Спасибо Тима за Jazzmin.",  # Приветственное сообщение
    "copyright": "Acme Library Ltd",  # Копирайт
    "search_model": ["auth.User", "auth.Group"],  # Модели для поиска
    "show_sidebar": True,  # Показывать боковую панель
    "navigation_expanded": True,  # Развернутая навигация
    "icons": {  # Иконки
        "auth": "fas fa-users-cog",  # Иконка для раздела "auth"
        "auth.user": "fas fa-user",  # Иконка для модели "auth.user"
        "auth.Group": "fas fa-users",  # Иконка для модели "auth.Group"
    },
    "default_icon_parents": "fas fa-chevron-circle-right",  # Иконка для родительских элементов по умолчанию
    "default_icon_children": "fas fa-circle",  # Иконка для дочерних элементов по умолчанию
    "related_modal_active": False,  # Активировать модальные окна для связанных объектов
    "use_google_fonts_cdn": True,  # Использовать CDN Google Fonts
    "show_ui_builder": False,  # Показывать строитель пользовательского интерфейса
    "changeform_format": "horizontal_tabs",  # Формат страницы редактирования
    "changeform_format_overrides": {  # Переопределение формата страницы редактирования для определенных моделей
        "auth.user": "collapsible",  # Использовать сворачиваемые вкладки для модели "auth.user"
        "auth.group": "vertical_tabs",  # Использовать вертикальные вкладки для модели "auth.group"
    },
    "language_chooser": False,  # Показывать выбор языка
}

