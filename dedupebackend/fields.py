from django import forms
from django.db.models import ForeignKey, OneToOneField, Field
from django.db.models.fields.files import FieldFile, FileDescriptor
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import File
from django.template.loader import render_to_string
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.safestring import mark_safe

from dedupebackend.backend import DedupedStorage
from dedupebackend import settings
from dedupebackend.models import UniqueFile

class UniqueFileAdminWidget(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        print 'UniqueFileWidget', args, kwargs
        self.choices = []
        # limit_choices_to = kwargs.pop('limit_choices_to', {})
        # queryset = kwargs.pop('queryset', [])
        # max_length = kwargs.pop('max_length', settings.MAX_FILENAME_LENGTH)
        # to_field_name = kwargs.pop('to_field_name', None)

        super(UniqueFileAdminWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'is_initial': False,
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_checkbox_label': self.clear_checkbox_label,
            'value': value
        }
        if self.is_initial(value):
            context['is_initial'] = True
            context['is_required'] = self.is_required

        return mark_safe(render_to_string('dedupebackend/uniquefield.html', context))

    def value_from_datadict(self, data, files, name):
        val = super(UniqueFileAdminWidget, self).value_from_datadict(data, files, name)
        if val is None:
            print "HELP HET IS FUCKING NOEN", data, data.get(name + '_id')
            return data.get(name + '_id')

        return val

    #     print 'het value uit die datadict is niks ait', val
    #     if val is False:
    #         return None
    #     return val

    # def get_template_substitution_values(self, value):
    #     """
    #     Return value-related substitutions.
    #     """
    #     return {
    #         'initial': conditional_escape(value),
    #         'initial_url': conditional_escape(value.url),
    #     }

    # def is_initial(self, value):
    #     return bool(value)


class UniqueFileAdminField(forms.FileField):
    widget = UniqueFileAdminWidget

    def __init__(self, limit_choices_to=None, admin_site='admin', queryset=None, to_field_name=None, *args, **kwargs):
        self.limit_choices_to = limit_choices_to
        self.admin_site = admin_site
        
        super(UniqueFileAdminField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        print 'bound_data', data, initial
        return super(UniqueFileAdminField, self).bound_data(data, initial)

    def widget_attrs(self, widget):
        print 'hoe kut kan het zijnn'
        return {
            'limit_choices_to': self.limit_choices_to,
            'admin_site': self.admin_site
        }

    def to_python(self, data):
        if isinstance(data, basestring) and len(data) == 40:
            return UniqueFile(pk=data)
        return super(UniqueFileAdminField, self).to_python(data)
    # def has_changed(self, initial, data):
    #     return initial != data


class UniqueFileField(ForeignKey):

    def __init__(self, *args, **kwargs):
        self.storage =  DedupedStorage()
        kwargs['to'] = 'dedupebackend.UniqueFile'
        super(UniqueFileField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # raise Exception("kut dut", kwargs)
        raw_id_widget = kwargs.pop('widget', None)

        defaults = {
            'form_class': UniqueFileAdminField,
            'max_length': self.max_length,
        }
        # If a file has been provided previously, then the form doesn't require
        # that a new file is provided this time.
        # The code to mark the form field as not required is used by
        # form_for_instance, but can probably be removed once form_for_instance
        # is gone. ModelForm uses a different method to check for an existing file.
        if 'initial' in kwargs:
            defaults['required'] = False
            # raise Exception('wht the hell')
        if raw_id_widget is not None:
            defaults['admin_site'] = raw_id_widget.admin_site
            # raise Exception('error')
            # print raw_id_widget.admin_site

        defaults.update(kwargs)
        #print defaults
        return super(UniqueFileField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        print 'save_form_data', instance, data, isinstance(data, File)
        if data is False:
            data = None
        if isinstance(data, File):
            data = UniqueFile(pk=self.storage.save(None, data))

        super(UniqueFileField, self).save_form_data(instance, data)

    def value_from_object(self, instance):
        return getattr(instance, self.name)
        # s = super(UniqueFile, self).value_from_object(instance)
        # print s, type(s)
        # raise Exception('henk')
        # return FieldFile(instance, self, getattr(instance, self.name).pk)
