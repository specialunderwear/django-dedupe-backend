from os.path import join
from django.conf import settings as s

STORAGE_PATH = getattr(s, 'GITBACKEND_STORAGE_PATH', join(s.MEDIA_ROOT, 'gitbackend'))
STORAGE_URL = getattr(s, 'GITBACKEND_STORAGE_URL', join(s.MEDIA_URL, 'gitbackend'))
AUTHOR = getattr(s, 'GITBACKEND_AUTHOR', 'django')
AUTHOR_EMAIL = getattr(s, 'GITBACKEND_AUTHOR_EMAIL', s.DEFAULT_FROM_EMAIL)
HASH_BLOCKSIZE = getattr(s, 'GITBACKEND_HASH_BLOCKSIZE', 65536)
MAX_FILENAME_LENGTH = getattr(s, 'GITBACKEND_MAX_FILENAME_LENGTH', 512)