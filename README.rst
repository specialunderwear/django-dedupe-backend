Deduplicate your uploaded file
------------------------------

If making sure your file uploads are never duplicated is more important than
organising your files into neat folders, you might want to try this package.

Usage
=====

You can use the storage backend on a global level by adding the following to
your django settings::

    DEFAULT_FILE_STORAGE = 'dedupebackend.storage.DedupedStorage'

If you want to use the other features offered by dedupebackend, you need to add
dedupebackend to ``INSTALLED_APPS`` like this::

    INSTALLED_APPS = [
        'dedupebackend',  # does not matter what spot
        ...
    ]

Admin integration
+++++++++++++++++

Adding dedupebackend to ``INSTALLED_APPS`` gives you an admin page where you
can check your uploaded files. I allready let you know dedupebackend just
throws verything in a large folder, but that does not mean you can not add
structure to the storage. Just not on a filesystem level. You should add
structure by adding relations to other models. It is easy enough to add
categories or something::

    class FileCategory(models.Model):
        files = models.ManyToManyField('dedupebackend.UniqueFile')
        name = models.TextField()

If you want to add a filter to the dedupebackend admin, try something like
this::

    from dedupebackend.admin import UniqueFileAdmin
    from dedupebackend.models import UniqueFile

    admin.site.unregister(UniqueFile)
    
    class CategoryUniqueFileAdmin(UniqueFileAdmin):
        list_filter = UniqueFileAdmin.list_filter + ('filecategory__name',)

    admin.site.register(UniqueFile, CategoryUniqueFileAdmin)

that might need some work, I never tested it :p

fields
++++++

There are some fields in dedupebackend you can use instead of the django
``FileField`` and ``ImageField``. You get a picker added to that, you can use
to select a file from the existing uploaded files.

Use something like this::

    from dedupebackend.fields import *

    class KoeHenkModel(model.Model):
        name = models.TextField()
        file = UniqueFileField("A normal file, nothing special")
        image = UniqueImageField("an image")

How does it work?
=================

Well, for each uploaded file, dedupebackend creates a file on disk named after
the hash of the file. Mostly the same as git does (I actually tried to use
libgit2 for this, but git is bad with deletions). Next to that file, a table
holds a record with some information about the file. The primary key of this
table is the hash value of the file. So it is really impossible to add
duplicates (but but, hash collisions).

The fields actually render a file form field on a foreign key model field.
The storage backend returns the hash value as the file name. And it can return
file objects when given such a hash value.
