from os.path import join
from django.conf import settings as s

STORAGE_PATH = getattr(s, 'DEDUPE_STORAGE_PATH', join(s.MEDIA_ROOT, 'dedupebackend'))
STORAGE_URL = getattr(s, 'DEDUPE_STORAGE_URL', join(s.MEDIA_URL, 'dedupebackend'))
AUTHOR = getattr(s, 'DEDUPE_AUTHOR', 'django')
AUTHOR_EMAIL = getattr(s, 'DEDUPE_AUTHOR_EMAIL', s.DEFAULT_FROM_EMAIL)
HASH_BLOCKSIZE = getattr(s, 'DEDUPE_HASH_BLOCKSIZE', 65536)
MAX_FILENAME_LENGTH = getattr(s, 'DEDUPE_MAX_FILENAME_LENGTH', 512)
