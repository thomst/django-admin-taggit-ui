# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltree import ModelTree
from taggit_ui.actions import tag_manager
from taggit_ui.actions import TagManager
from taggit_ui.filters import TagFilter
from .models import ModelA
from testapp.models import ModelOne, ModelTwo


class TagViewMixin:
    list_filter = [TagFilter]
    actions = [tag_manager]

    def tag_view(self, obj):
        return ", ".join(o.name for o in obj.tags.all()) or '-'
    tag_view.short_description = 'tags'


@admin.register(ModelA)
class ModelAAdmin(TagViewMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'model_b',
        'tag_view',
    )


@admin.register(ModelOne)
class ModelOneAdmin(TagViewMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'tag_view',
    )
    actions = [TagManager(ModelTree)]

    def tag_view(self, obj):
        return ", ".join(o.name for o in obj.xtags.all()) or '-'
    tag_view.short_description = 'tags'


@admin.register(ModelTwo)
class ModelTwoAdmin(TagViewMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'tag_view',
    )

    def tag_view(self, obj):
        return ", ".join(o.name for o in obj.xtags.all()) or '-'
    tag_view.short_description = 'tags'
