import os
import dj_database_url
from .base import *

DEBUG = False
ALLOWED_HOSTS = [".pycon.ca"]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, os.pardir, "public", "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, os.pardir, "public", "static")
STATIC_URL = "/static/"

MIDDLEWARE_CLASSES = ['django.middleware.security.SecurityMiddleware'] + MIDDLEWARE_CLASSES
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Symposion

DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

# Mailgun
EMAIL_BACKED = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ['MAILGUN_ACCESS_KEY']
MAILGUN_SERVER_NAME = 'mailgun.pycon.ca'
