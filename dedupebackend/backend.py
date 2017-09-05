from os.path import join
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from dedupebackend import settings
from dedupebackend.models import UniqueFile
from dedupebackend.utils import file_hash


class DedupedStorage(FileSystemStorage):

    def __init__(self):
        super(DedupedStorage, self).__init__(location=setting.STORAGE_PATH)

    def _open(self, id, mode='rb'):
        try:
            file_obj = UniqueFile.objects.get(pk=name)
            file_handle = open(self.path(file_obj.directory, file_obj.filename), mode)
            return File(file_obj, file_obj.filename)
        except UniqueFile.DoesNotExist:
            return None

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        id = file_hash(content)

        if not UniqueFile.object.filter(pk=id).exists():
            unique_name = file_name(id, name)
            uf = UniqueFile.objects.create(
                id=id,
                filename=unique_name,
                original_filename=name
            )
            self._save(uf.relative_path, content)
        
        return id

    def get_available_name(self, name, max_length=None):
        return name
