# config/settings.py

import os
from pathlib import Path

# ===== БАЗОВЫЕ НАСТРОЙКИ =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== БЕЗОПАСНОСТЬ =====
SECRET_KEY = 'django-insecure-change-this-key-in-production-123456789'

# Режим отладки (для разработки)
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ===== ПРИЛОЖЕНИЯ =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ===== ШАБЛОНЫ =====
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

# ===== БАЗА ДАННЫХ =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===== ВАЛИДАЦИЯ ПАРОЛЕЙ =====
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

# ===== ИНТЕРНАЦИОНАЛИЗАЦИЯ =====
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ===== СТАТИЧЕСКИЕ ФАЙЛЫ =====
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== НАСТРОЙКИ EMAIL =====
# Для тестирования используем консольный бэкенд (письма будут в консоли)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Администраторы для получения писем об ошибках
ADMINS = [
    ('Admin', 'admin@example.com'),
]
SERVER_EMAIL = 'noreply@example.com'

# ==============================================
# ===== НАСТРОЙКИ ЛОГИРОВАНИЯ =====
# ==============================================

import logging

# Создаем папку logs, если ее нет
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ===== ФИЛЬТРЫ =====
    'filters': {
        # Фильтр для DEBUG режима
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # Фильтр для PRODUCTION режима (не DEBUG)
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        # Фильтр только для security логов
        'only_security': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.name.startswith('django.security')
        },
        # Фильтр только для ERROR и CRITICAL
        'only_error_critical': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno >= logging.ERROR
        },
    },

    # ===== ФОРМАТТЕРЫ =====
    'formatters': {
        # Для DEBUG и INFO в консоли
        'console_debug': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для WARNING и выше (с pathname)
        'console_warning': {
            'format': '{asctime} - {levelname} - {pathname} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для ERROR и CRITICAL (со стеком)
        'console_error': {
            'format': '{asctime} - {levelname} - {pathname} - {message}\n{exc_info}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для general.log
        'general': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для errors.log
        'errors': {
            'format': '{asctime} - {levelname} - {pathname} - {message}\n{exc_info}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для security.log
        'security': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Для email
        'email': {
            'format': '{asctime} - {levelname} - {pathname} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    # ===== ОБРАБОТЧИКИ =====
    'handlers': {
        # ----- Консольные обработчики (только при DEBUG=True) -----
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'console_debug',
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'console_error',
        },

        # ----- Файловые обработчики -----
        # general.log (только при DEBUG=False)
        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'general.log'),
            'filters': ['require_debug_false'],
            'formatter': 'general',
            'encoding': 'utf-8',
        },
        # errors.log (только ERROR и CRITICAL)
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'filters': ['only_error_critical'],
            'formatter': 'errors',
            'encoding': 'utf-8',
        },
        # security.log (только django.security)
        'security_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'filters': ['only_security'],
            'formatter': 'security',
            'encoding': 'utf-8',
        },

        # ----- Email обработчик (только при DEBUG=False) -----
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'email',
            'include_html': False,
        },
    },

    # ===== ЛОГГЕРЫ =====
    'loggers': {
        # Основной логгер django
        'django': {
            'handlers': [
                'console_debug',
                'console_warning',
                'console_error',
                'general_file'
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Логгеры для errors.log
        'django.request': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер для security.log
        'django.security': {
            'handlers': ['security_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}