# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import ModelA
from taggit_ui.actions import manage_tags
from taggit_ui.filters import TagFilter


@admin.register(ModelA)
class ModelAAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'model_b',
        'tag_view',
    )
    list_filter = [TagFilter]
    actions = [manage_tags]

    def tag_view(self, obj):
        return ", ".join(o.name for o in obj.tags.all()) or '-'
    tag_view.short_description = 'tags'
