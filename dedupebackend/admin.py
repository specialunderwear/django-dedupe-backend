from django.contrib import admin
from dedupebackend.fields import UniqueFileAdminField, UniqueFileAdminWidget
from dedupebackend.models import UniqueFile
from dedupebackend.utils import sizeof_fmt
from dedupebackend.filters import FileSizeFilter
from django.utils.safestring import mark_safe


class UniqueFileAdmin(admin.ModelAdmin):
    search_fields = ('original_filename', 'filename')
    list_display = ('original_filename', 'mime_type', 'filesize', 'id', 'tiny_thumb')
    list_filter = ('mime_type', FileSizeFilter)

    def has_add_permission(self, request):
        return False

    def filesize(self, obj):
        if obj.size is not None:
            return sizeof_fmt(obj.size)
        return 'Unknown'

    def tiny_thumb(self, obj):
        return mark_safe('<img src="%s" alt="%s" style="max-width:30px; max-height:30px;"/>' % (obj.url, obj.original_filename))

admin.site.register(UniqueFile, UniqueFileAdmin)