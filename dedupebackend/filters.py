from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class FileSizeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('file size')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'filesize'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('unknown', _('Unknown')),
            ('10kb', _('10 kilobytes')),
            ('100kb', _('100 kilobytes')),
            ('1mb', _('1 megabytes')),
            ('10mb', _('10 megabytes')),
            ('large', _('Very large files'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'unknown':
            return queryset.filter(size__isnull=True)
        if self.value() == '10kb':
            return queryset.filter(size__lte=10240)
        if self.value() == '100kb':
            return queryset.filter(size__gt=10240,
                                    size__lte=102400)
        if self.value() == '1mb':
            return queryset.filter(size__gt=102400,
                                    size__lte=1048576)
        if self.value() == '10mb':
            return queryset.filter(size__gt=1048576,
                                    size__lte=10485760)
        if self.value() == 'large':
            return queryset.filter(size__gt=10485760)

        return queryset
        