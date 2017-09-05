from django.db.fields import CharField
from pygit2 import Oid


class OidField(CharField):
    description = "A field that represents a libgit oid"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super(HandField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(HandField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Oid(value)

    def to_python(self, value):
        if isinstance(value, Oid):
            return value

        if value is None:
            return value

        return Oid(value)

    def get_prep_value(self, value):
        return unicode(value)
