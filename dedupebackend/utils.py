from os.path import splitext
import hashlib
from dedupebackend import settings


def file_hash(content):
    hasher = hashlib.sha1()
    buf = content.read(settings.HASH_BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = content.read(settings.HASH_BLOCKSIZE)

    content.seek(0)
    return hasher.hexdigest()

def file_name(id, name):
    _, ext = splitext(name):
    return "%s%s" % id, ext
