# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from taggit_ui.forms import ManageTagsForm


def manage_tags(modeladmin, request, queryset):
    # TODO: check if model is tagable!

    add = 'add_tags' in request.POST
    remove = 'remove_tags' in request.POST

    if add or remove:
        form = ManageTagsForm(request.POST)
    else:
        form = ManageTagsForm()

    if form.is_valid():
        tags = form.cleaned_data['tags']
        for obj in queryset:
            if add:
                obj.tags.add(*tags)
            elif remove:
                obj.tags.remove(*tags)

        return HttpResponseRedirect(request.get_full_path())

    else:
        return render(request, 'admin/manage-tags-form.html', {
            'objects': queryset.order_by('pk'),
            'form': form,
            'title': 'Manage Tags'
            })
