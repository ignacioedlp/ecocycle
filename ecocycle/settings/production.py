from .base import *
import os
import dj_database_url
from pathlib import Path
from ecocycle.logging import *
from dotenv import load_dotenv 

load_dotenv(Path.joinpath(BASE_DIR, '.env'))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [ '*' ]

API_URL = os.environ.get('API_URL')

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'