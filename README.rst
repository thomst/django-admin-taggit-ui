=================================
Welcome to django-admin-taggit-ui
=================================

.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
   :target: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
   :alt: python: 3.8, 3.9, 3.10,3.11,3.12,3.13

.. image:: https://img.shields.io/badge/django-3.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange
   :target: https://img.shields.io/badge/django-3.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange
   :alt: django: 3.0, 3.1, 3.2, 4.0, 4.1, 4.2, 5.0, 5.1,5.2,6.0

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


Setup
=====
Add more_admin_filters to your installed apps::

    INSTALLED_APPS = [
        'taggit_ui',
        ...
    ]

Extend your :code:`url_patterns` in urls.py::

    urlpatterns = [
        ...
        url(r'^', include('taggit_ui.urls')),
    ]

Add the :code:`TagFilter` and :code:`manage_tag` action to your ModelAdmin::

    from taggit_ui.filters import TagFilter
    from taggit_ui.actions import tag_manager

    class MyModelAdmin(admin.ModelAdmin):
        ...
        list_filter = [
            TagFilter,
            ...
        ]
        actions = [
            tag_manager,
            ...
        ]

It is possible to optionally tag related items of other models using the admin
action. Therefore initialize the :code:`TagManager`` class with a
`ModelTree <https://github.com/thomst/django-modeltree>`_::

    from taggit_ui.actions import TagManager
    from modeltree import ModelTree

    class MyModelAdmin(admin.ModelAdmin):
        ...
        actions = [
            TagManager(ModelTree),
            ...
        ]

The admin action will then render its form with all taggible related Models as
checkbox fields and the count of related items belonging to these models.
