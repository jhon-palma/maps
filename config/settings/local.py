from .base import *

DJANGO_DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]