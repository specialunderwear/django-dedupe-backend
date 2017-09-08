from django.core.files import File

from dedupebackend.models import UniqueFile
from dedupebackend.utils import (
    SpecificNameStorage,
    get_or_create_from_file
)


class DedupedStorage(SpecificNameStorage):

    def _open(self, id, mode='rb'):
        try:
            file_obj = UniqueFile.objects.get(pk=id)
            file_handle = open(self.path(file_obj.relative_path), mode)
            return File(file_handle, file_obj.filename)
        except UniqueFile.DoesNotExist:
            return None

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        uf, _ = get_or_create_from_file(name, content, self, UniqueFile, UniqueFile.objects)
        return uf.id

    def url(self, name):
        uf = UniqueFile.objects.get(id=name)
        return uf.get_absolute_url()
