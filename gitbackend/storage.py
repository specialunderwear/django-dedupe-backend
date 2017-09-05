import os
from os.path import join, dirname, splitext
from django.conf import settings
from pygit2 import init_repository, hashfile, GIT_FILEMODE_BLOB, Signature
import threading

from gitbackend.settings import STORAGE_PATH, AUTHOR, AUTHOR_EMAIL

sig = Signature(AUTHOR, AUTHOR_EMAIL)
# >>> author = Signature('Alice Author', 'alice@authors.tld')
# >>> committer = Signature('Cecil Committer', 'cecil@committers.tld')
# >>> tree = repo.TreeBuilder().write()
# >>> repo.create_commit(
# ... 'refs/heads/master', # the name of the reference to update
# ... author, committer, 'one line commit message\n\ndetailed commit message',
# ... tree, # binary string representing the tree object ID
# ... [] # list of binary strings representing parents of the new commit
# ... )


class ObjectStorage(threading.local):
    def __init__(self):
        self.repo = init_repository(STORAGE_PATH, bare=True)
        if self.repo.is_empty:
            self.repo.TreeBuilder().write()
        # self.repo.create_reference("ref/heads/master", None)

    @property
    def head(self):
        if self.repo.is_empty:
            return []
        return [self.repo.head.target]
        
    def add_file(self, path):
        oid = hashfile(path)
        print oid
        if oid in self.repo:
            print "HIJ BESTAAT AL"
            return oid
        _, ext = splitext(path)
        _oid = self.repo.create_blob_fromdisk(path)
        assert(_oid == oid)
        print oid
        builder = self.repo.TreeBuilder()
        builder.insert("%s%s" % (join(str(oid)[:2], str(oid)[2:]), ext), oid, GIT_FILEMODE_BLOB)
        tree = builder.write()
        return self.repo.create_commit(
            'refs/heads/master',
            sig, sig,
            'added file %s' % path,
            tree,
            self.head
        )

    def exists(self, oid):
        return oid in self.repo

    def delete(self, oid):
        path = self.location(oid)
        if path is not None:
            os.remove(path)
            try:
                os.rmdir(dirname(path))
            except OSError:
                pass
            return True

        return False

    def location(self, oid):
        try:
            document_root, path = self.directory_path(oid)
            return join(document_root, path)
        except ValueError:
            return None

    def directory_path(self, object_id):
        full_id = self.repo.git_object_lookup_prefix(object_id).hex
        return (join(self.repo.path, 'objects'), join(full_id[:2], full_id[2:]))


objectstore = ObjectStorage()

def kut():
    repo = objectstore.repo
    print repo.is_empty
    # print repo.head
    print list(repo.listall_references())
    print dir(repo)
    print objectstore.add_file('/tmp/gitsizetest/henk.jpg')
    # print repo.lookup_reference("refs/heads/master")
    print repo['b97d938032a994caab023cf822a0e114240ca3a4']
    # print objectstore.delete('b97d938032a994caab023cf822a0e114240ca3a4')
