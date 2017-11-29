from os.path import join

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dedupebackend.utils import (
    get_or_create_from_file,
    get_directory_from_file_id,
    SpecificNameStorage
)
from dedupebackend import settings


class UniqueFileManager(models.Manager):
    use_in_migrations = True

    def get_or_create_from_file(self, name, content):
        storage = SpecificNameStorage()
        return get_or_create_from_file(name, content, storage, self.model, self)


class UniqueFile(models.Model):
    objects = UniqueFileManager()

    id = models.CharField(max_length=40, primary_key=True)
    filename = models.CharField(max_length=50, unique=True)
    original_filename = models.CharField(max_length=settings.MAX_FILENAME_LENGTH, blank=True, null=True)
    size = models.IntegerField(null=True)
    mime_type = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return "%s" % self.original_filename

    def __nonzero__(self):
        return bool(self.pk)

    @property
    def path(self):
        return join(self.directory, self.filename)

    @property
    def path_full(self):
        return join(settings.STORAGE_PATH, self.path)

    def get_absolute_url(self):
        return join(settings.STORAGE_URL, self.path)

    @property
    def url(self):
        if self.pk is not None:
            return self.get_absolute_url()

        return None

    @property
    def directory(self):
        return get_directory_from_file_id(self.id)

    class Meta:
        verbose_name = _('Unique, deduplicated file')
        verbose_name_plural = _('Unique files')
