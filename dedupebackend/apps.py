from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DedupeBackendConfig(AppConfig):
    name = 'dedupebackend'
    verbose_name = _("File storage")
