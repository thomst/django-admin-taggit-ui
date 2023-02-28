# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from modeltree import ModelTree
from taggit.managers import TaggableManager
from taggit_ui.forms import ManageTagsForm
from taggit_ui.forms import IncludeForm


class TaggibleModelTree(ModelTree):
    @property
    def is_taggible(self):
        return bool(self.tag_manager)

    @property
    def tag_manager(self):
        if not hasattr(self, '_tag_manager'):
            self._tag_manager = None
            for field in self.model._meta.get_fields():
                if isinstance(field, TaggableManager):
                    self._tag_manager = field.name
        return self._tag_manager

    @property
    def form_field(self):
        form_field = forms.BooleanField(
            label=self.label_path,
            required=False)
        return form_field

    def process_tags(self, task, tags):
        if self.is_taggible:
            for item in self.items:
                getattr(getattr(item, self.tag_manager), task)(*tags)

    def iterate_taggible(self):
        filter = lambda n: n.is_taggible
        return self.iterate(filter=filter)

    def build_form_class(self):
        fields = dict()
        for node in self.iterate_taggible():
            fields[self.field_path] = self.form_field
        # If we have no children we hide the root-form-field.
        if not self.children:
            fields[self.field_path].initial = True
            fields[self.field_path].widget = forms.HiddenInput
        return type('IncludeForm', (IncludeForm,), fields)


class TagManager:
    def __init__(self, follow_relatetions=None):
        self.follow_relatetions = follow_relatetions

    def __call__(self, modeladmin, request, queryset):
        # Create model-tree and form-class.
        if self.follow_relatetions:
            class_params = dict(FIELD_PATHS=self.follow_relatetions)
        else:
            class_params = dict(MAX_LEVEL=0)
        tree_class = type('Tree', (TaggibleModelTree,), class_params)
        modeltree = tree_class(modeladmin.model, queryset)
        include_form_class = modeltree.build_form_class()

        # Initialize forms.
        task = 'add' in request.POST and 'add' or 'remove' in request.POST and 'remove'
        if task:
            tag_form = ManageTagsForm(request.POST)
            include_form = include_form_class(request.POST)
        else:
            tag_form = ManageTagsForm()
            include_form = include_form_class()

        # Render the forms.
        if not tag_form.is_valid() or not include_form.is_valid():
            return render(request, 'admin/manage-tags-form.html', {
                'objects': queryset.order_by('pk'),
                'tag_form': tag_form,
                'include_form': include_form,
                'title': 'Manage Tags'
                })

        # Set tags.
        tags = tag_form.cleaned_data['tags']
        includes = [k for k, v in include_form.cleaned_data if v]
        for node in modeltree.iterate(filter=lambda n: n.name in includes):
            node.process_tags(task, tags)

        return HttpResponseRedirect(request.get_full_path())
