import logging
from django.core.files import File

from dedupebackend.models import UniqueFile
from dedupebackend.utils import (
    SpecificNameStorage,
    get_or_create_from_file
)

logger = logging.getLogger(__name__)


class DedupedStorageFile(File):
    """
    A file plus some data.
    """
    def __init__(self, file, data, name=None):
        self.data = data
        super(DedupedStorageFile, self).__init__(file, name)

    @property
    def url(self):
        return self.data.url

class DedupedStorage(SpecificNameStorage):

    def _open(self, id, mode='rb'):
        try:
            file_obj = UniqueFile.objects.get(pk=id)
            file_handle = open(self.path(file_obj.path), mode)
            return DedupedStorageFile(file_handle, file_obj, file_obj.filename)
        except UniqueFile.DoesNotExist:
            return None

    def create_or_load(self, name, content, max_length=None):
        if name is None:
            name = content.name

        uf, created = get_or_create_from_file(name, content, self, UniqueFile, UniqueFile.objects)
        logger.debug("%s was created? %s" % (name, created))
        return uf, created

    def save(self, name, content, max_length=None):
        uf, _ = self.create_or_load(name, content, max_length)
        return uf.id

    def url(self, name):
        uf = UniqueFile.objects.get(id=name)
        return uf.get_absolute_url()
