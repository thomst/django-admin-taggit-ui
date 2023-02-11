=================================
Welcome to django-admin-taggit-ui
=================================

Description
===========
This app provides a tag-filter and an admin-action to handle tags created with
`taggit` within the django admin backend.


Installation
============
Install from pypi.org::

    pip install django-admin-taggit-ui

Add more_admin_filters to your installed apps::

    INSTALLED_APPS = [
        'taggit_ui',
        ...
    ]

Add the `TagFilter` and `manage_tag` action to your ModelAdmin::

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
