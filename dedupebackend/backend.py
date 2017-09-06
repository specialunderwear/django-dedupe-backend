from os.path import basename
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.urlresolvers import reverse

from dedupebackend import settings
from dedupebackend.models import UniqueFile
from dedupebackend.utils import file_hash, file_name

class DedupedStorage(FileSystemStorage):

    def __init__(self):
        super(DedupedStorage, self).__init__(location=settings.STORAGE_PATH)

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

        id = file_hash(content)

        if not UniqueFile.objects.filter(pk=id).exists():
            unique_name = file_name(id, name)
            uf = UniqueFile.objects.create(
                id=id,
                filename=unique_name,
                original_filename=basename(name)[:settings.MAX_FILENAME_LENGTH]
            )
            try:
                self._save(uf.relative_path, content)
            except IOError:
                pass
        
        return id

    def get_available_name(self, name, max_length=None):
        return name

    def url(self, name):
        uf = UniqueFile.objects.get(id=name)
        return uf.get_absolute_url()
