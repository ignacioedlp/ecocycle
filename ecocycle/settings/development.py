from .base import *
import os
import dj_database_url
from pathlib import Path

load_dotenv(Path.joinpath(BASE_DIR, '.env'))

SECRET_KEY = 'django-insecure-si3xzq-*^r8gutunm1uk$)a$2n6&1*zjqp%vlb2g=@clujn!hm'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
