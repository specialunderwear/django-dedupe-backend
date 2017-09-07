from os.path import join, basename
from django.db import models
from dedupebackend import settings

class UniqueFile(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    filename = models.CharField(max_length=50, unique=True)
    original_filename = models.CharField(max_length=settings.MAX_FILENAME_LENGTH, blank=True, null=True)
    size = models.IntegerField(null=True)
    mime_type = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return "%s" % self.original_filename

    def __nonzero__(self):
        return bool(self.pk)

    def get_absolute_url(self):
        return join(settings.STORAGE_URL, self.relative_path)

    @property
    def url(self):
        if self.pk is not None:
            return self.get_absolute_url()

        return None

    @property
    def directory(self):
        return self.id[:2]

    @property
    def relative_path(self):
        return join(self.directory, self.filename)

    class Meta:
        verbose_name = 'Unique, deduplicated file'
        verbose_name_plural = 'Unique files'
