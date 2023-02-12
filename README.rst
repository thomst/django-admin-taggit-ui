=================================
Welcome to django-admin-taggit-ui
=================================

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue
   :target: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue
   :alt: python: 3.6, 3.7, 3.8, 3.9, 3.10

.. image:: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1-orange
   :target: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1-orange
   :alt: django: 2.2, 3.0, 3.1, 3.2, 4.0, 4.1

.. image:: https://github.com/thomst/django-admin-taggit-ui/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/thomst/django-admin-taggit-ui/actions/workflows/ci.yml
   :alt: Run tests for django-admin-taggit-ui

.. image:: https://coveralls.io/repos/github/thomst/django-admin-taggit-ui/badge.svg?branch=master
   :target: https://coveralls.io/github/thomst/django-admin-taggit-ui?branch=master
   :alt: Coveralls


Description
===========
This app is build in top of `django-taggit <https://github.com/jazzband/django-taggit>`_
and provides a tag-filter and an admin-action to handle tags with ease within
django's admin backend.

Tag-Filter
**********
The tag filter allows you to include and exclude mutliple tags as well as easily
deleting tags.

Admin-Action
************
The admin action allows you to easily add and remove tags from objects.


Installation
============
Install from pypi.org::

    pip install django-admin-taggit-ui

Add more_admin_filters to your installed apps::

    INSTALLED_APPS = [
        'taggit_ui',
        ...
    ]

Add the :code:`TagFilter` and :code:`manage_tag` action to your ModelAdmin::

    from taggit_ui.filters import TagFilter
    from taggit_ui.actions import manage_tags

    class MyModelAdmin(admin.ModelAdmin):
        ...
        list_filter = [
            TagFilter,
            ...
        ]
        actions = [
            manage_tags,
            ...
        ]

Extend your `url_patterns` in urls.py::

    urlpatterns = [
        ...
        url(r'^', include('taggit_ui.urls')),
    ]


Limitations
===========
Currently this app only works with models that referencing their
:code:`TaggableManager` as an attribute named :code:`tags`::

    class MyModel(models.Model):
        tags = TaggableManager(blank=True)
        ...
