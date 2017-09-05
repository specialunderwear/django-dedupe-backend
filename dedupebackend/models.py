from os.path import join
from django.db import models
from dedupebackend import settings

class UniqueFile(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    filename = models.CharField(max_length=50, unique=True)
    original_filename = models.CharField(max_length=settings.MAX_FILENAME_LENGTH, blank=True, null=True)

    @property
    def directory(self):
        return self.id[:2]

    @property
    def relative_path(self):
        return join(self.directory, self.filename)

    class Meta:
        verbose_name = 'Unique, deduplicated file'
        verbose_name_plural = 'Unique files'
