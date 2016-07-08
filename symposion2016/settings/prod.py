import dj_database_url
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*.pycon.ca"]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, os.pardir, "public", "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, os.pardir, "public", "static")
STATIC_URL = "/static/"
