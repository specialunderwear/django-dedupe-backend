import hashlib
import logging
import os
import mimetypes
from os.path import splitext, exists, basename, join
from django.core.files.storage import FileSystemStorage

from dedupebackend import settings

logger = logging.getLogger(__name__)


def file_hash(content):
    hasher = hashlib.sha1()
    buf = content.read(settings.HASH_BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = content.read(settings.HASH_BLOCKSIZE)

    content.seek(0)
    return hasher.hexdigest()


def file_name(id, name):
    _, ext = splitext(name)
    return "%s%s" % (id, ext.lower())


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class SpecificNameStorage(FileSystemStorage):
    """
    Storage class that does not try to invent a new name when saving a file.
    """
    def __init__(self):
        super(SpecificNameStorage, self).__init__(location=settings.STORAGE_PATH)

    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        full_path = self.path(name)
        if not exists(full_path):
            return super(SpecificNameStorage, self)._save(name, content)
        return name


def get_directory_from_file_id(file_id):
    return file_id[:2]


def get_or_create_from_file(name, content, storage, model_class, model_manager):
    """
    To avoid code duplication in the model manager and the file storage
    backend, creating model and storing the file is defined in this utility.
    """
    file_id = file_hash(content)

    try:
        return model_manager.get(pk=file_id), False
    except model_class.DoesNotExist:
        unique_name = file_name(file_id, name)
        mimetype, _ = mimetypes.guess_type(name)
        size = os.fstat(content.fileno()).st_size
        uf = model_manager.create(
            id=file_id,
            filename=unique_name,
            original_filename=basename(name)[:settings.MAX_FILENAME_LENGTH],
            mime_type=mimetype,
            size=size
        )

        directory = get_directory_from_file_id(file_id)
        path = join(directory, uf.filename)
        stored_location = storage._save(path, content)
        logger.debug("File stored in %s" % stored_location)

        return uf, True
