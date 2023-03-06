# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from modeltree import ModelTree
from taggit.managers import TaggableManager
from taggit_ui.forms import ManageTagsForm
from taggit_ui.forms import IncludeForm


class TaggitUiModelTreeMixin:
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

    def process_tags(self, task, tags):
        if self.is_taggible:
            for item in self.items:
                getattr(getattr(item, self.tag_manager), task)(*tags)

    def iterate_taggible(self):
        filter = lambda n: n.is_taggible
        return self.iterate(filter=filter)

    @property
    def form_field(self):
        form_field = forms.BooleanField(
            label=' '.join(str(n) for n in self.path),
            required=False)
        return form_field

    def build_form_class(self):
        fields = dict()
        for node in self.iterate_taggible():
            fields[node.field_path] = node.form_field
        if not self.root.children:
            fields['root'].widget = forms.HiddenInput(attrs=dict(value=True))
        return type('IncludeForm', (IncludeForm,), fields)


class FlatModelTree(ModelTree):
    MAX_DEPTH = 0


def manage_tags(modeladmin, request, queryset):
    # Create model-tree and form-class.
    base_tree_class = getattr(modeladmin, 'taggit_ui_modeltree', FlatModelTree)
    tree_class = type('TaggitUiTree', (base_tree_class, TaggitUiModelTreeMixin), dict())
    modeltree = tree_class(modeladmin.model, queryset)
    include_form_class = modeltree.build_form_class()
    show_include_form = bool(modeltree.children)

    # Initialize forms.
    task = 'add' in request.POST and 'add' or 'remove' in request.POST and 'remove'
    if task:
        tag_form = ManageTagsForm(request.POST)
        include_form = include_form_class(request.POST)
    else:
        tag_form = ManageTagsForm()
        include_form = include_form_class(initial=dict(root=True))

    # Render the forms.
    if not tag_form.is_valid() or not include_form.is_valid():
        return render(request, 'admin/manage-tags-form.html', {
            'objects': queryset.order_by('pk'),
            'tag_form': tag_form,
            'include_form': include_form,
            'show_include_form': show_include_form,
            'title': 'Manage Tags'
            })

    # Set tags.
    tags = tag_form.cleaned_data['tags']
    includes = [k for k, v in include_form.cleaned_data.items() if v]
    for node in modeltree.iterate(filter=lambda n: n.field_path in includes):
        node.process_tags(task, tags)

    return HttpResponseRedirect(request.get_full_path())
