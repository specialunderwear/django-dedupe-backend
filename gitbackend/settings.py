from os.path import join
from django.conf import settings as s

STORAGE_PATH = getattr(s, 'GITBACKEND_STORAGE_PATH', join(s.MEDIA_ROOT, 'gitbackend'))
AUTHOR = getattr(s, 'GITBACKEND_AUTHOR', 'django')
AUTHOR_EMAIL = getattr(s, 'GITBACKEND_AUTHOR_EMAIL', s.DEFAULT_FROM_EMAIL)
