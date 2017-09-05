from django.db import models

from gitbackend.fields import OidField


class GitStorageFile(models.Model):
    oid = OidField(primary_key=True)
    filename = models.CharField(max_length=512)

