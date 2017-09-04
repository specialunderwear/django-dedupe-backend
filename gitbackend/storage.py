from os.path import join
from django.conf import settings
from pygit2 import init_repository
import threading


class FileStorage(threading.local):
    def __init__(self, storage_path):
        self.repo = init_repository(storage_path, bare=True)

    def add_file(self, path):
        return self.repo.create_blob_fromdisk(path)

    def location(self, object_id):
        try:
            document_root, path = self.directory_path(object_id)
            return join(document_root, path)
        except ValueError:
            return None

    def directory_path(self, object_id):
        full_id = self.repo.git_object_lookup_prefix(object_id).hex
        return (join(self.repo.path, 'objects'), join(full_id[:2], full_id[2:]))


objectstore = ObjectStorage()
