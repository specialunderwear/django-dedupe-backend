from django.contrib import admin
from .models import UniqueFile

class UniqueFileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UniqueFile, UniqueFileAdmin)