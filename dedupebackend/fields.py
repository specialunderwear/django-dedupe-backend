from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.files.base import File
from django.db.models import ForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from dedupebackend.storage import DedupedStorage
from dedupebackend.models import UniqueFile


class UniqueFileAdminWidget(forms.ClearableFileInput):
    template_name = 'dedupebackend/uniquefield.html'

    def __init__(self, *args, **kwargs):
        super(UniqueFileAdminWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'is_initial': False,
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_checkbox_label': self.clear_checkbox_label,
            'value': value,
            'is_required': self.is_required
        }
        if self.is_initial(value):
            context['is_initial'] = True

        return mark_safe(render_to_string(self.template_name, context))

    def raw_id_field_name(self, name):
        return "%s-id" % name

    def value_from_datadict(self, data, files, name):
        val = super(UniqueFileAdminWidget, self).value_from_datadict(data, files, name)
        if val is None:
            return data.get(self.raw_id_field_name(name))

        return val

    class Media:
        css = {
            'all': ('dedupebackend/uniquefield.css',)
        }

class UniqueFileAdminField(forms.FileField):
    widget = UniqueFileAdminWidget

    def __init__(self, limit_choices_to=None, admin_site='admin', queryset=None, to_field_name=None, *args, **kwargs):
        self.limit_choices_to = limit_choices_to
        self.admin_site = admin_site
        
        super(UniqueFileAdminField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        return super(UniqueFileAdminField, self).bound_data(data, initial)

    def widget_attrs(self, widget):
        return {
            'limit_choices_to': self.limit_choices_to,
            'admin_site': self.admin_site
        }

    def to_python(self, data):
        if isinstance(data, basestring) and len(data) == 40:
            return data

        return super(UniqueFileAdminField, self).to_python(data)


class UniqueFileField(ForeignKey):
    form_class = UniqueFileAdminField

    def __init__(self, *args, **kwargs):
        self.storage =  DedupedStorage()
        kwargs['to'] = 'dedupebackend.UniqueFile'
        super(UniqueFileField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        raw_id_widget = kwargs.pop('widget', None)
        if not isinstance(raw_id_widget, ForeignKeyRawIdWidget):
            raise Exception('Please add the UniqueFileField to raw_id_fields')

        defaults = {
            'form_class': self.form_class,
            'max_length': self.max_length,
            'admin_site': raw_id_widget.admin_site
        }

        # If a file has been provided previously, then the form doesn't require
        # that a new file is provided this time.
        # The code to mark the form field as not required is used by
        # form_for_instance, but can probably be removed once form_for_instance
        # is gone. ModelForm uses a different method to check for an existing file.
        if 'initial' in kwargs:
            defaults['required'] = False

        defaults.update(kwargs)

        return super(UniqueFileField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        if data is False:
            data = None
        if isinstance(data, File):
            data = self.storage.save(None, data)
        if isinstance(data, basestring) and len(data) == 40:
            data = UniqueFile(pk=data)

        super(UniqueFileField, self).save_form_data(instance, data)

    def value_from_object(self, instance):
        return getattr(instance, self.name)


class UniqueImageAdminWidget(UniqueFileAdminWidget):
    template_name = 'dedupebackend/uniqueimagefield.html'


class UniqueImageAdminField(UniqueFileAdminField):
    widget = UniqueImageAdminWidget


class UniqueImageField(UniqueFileField):
    form_class = UniqueImageAdminField
