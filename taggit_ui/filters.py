# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.models import TaggedItem


class TagFilter(admin.SimpleListFilter):
    """
    TagFilter providing multiselect include and exclude option. Also allow to
    easily delete tags.
    """
    title = 'Tags'
    parameter_name = 'tags'
    template = 'admin/tag-filter.html'

    def values(self):
        if self.value():
            return self.value().split(',')
        else:
            return list()

    def lookups(self, request, model_admin):
        choices = list()
        for tag in TaggedItem.tags_for(model_admin.model):
            kwargs=dict(
                tag_id=tag.id,
                app_label=model_admin.model._meta.app_label,
                model_name=model_admin.model._meta.model_name)
            url_path = reverse('remove-tag-from-all-by-id', kwargs=kwargs)
            choices.append((tag.name, url_path))
        choices.sort()
        return choices

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        includes = [v[1:] for v in self.values() if v[0] == '+']
        excludes = [v[1:] for v in self.values() if v[0] == '-']
        if includes:
            queryset = queryset.filter(tags__name__in=includes)
        if excludes:
            queryset = queryset.exclude(tags__name__in=excludes)
        return queryset.distinct()

    def get_query_params(self, lookup):
        new_params = dict()
        remove = list()
        values = self.values()
        value = next(iter([l for l in values if l[1:] == lookup[1:]] + [None]))

        if not value:
            values.append(lookup)
        elif value == lookup:
            values.remove(value)
        elif not value == lookup:
            values.remove(value)
            values.append(lookup)

        if values:
            new_params[self.parameter_name] = ','.join(values)
        else:
            remove.append(self.parameter_name)

        return new_params, remove

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
        }
        for tag, url_path in self.lookup_choices:
            lookup = tag
            plus_lookup = '+' + lookup
            minus_lookup = '-' + lookup
            values = [v.lstrip('+-') for v in self.values()]
            yield {
                'display': tag,
                'url_path': url_path,
                'selected': self.value() and lookup in values,
                'plus': {
                    'selected': self.value() and plus_lookup in self.values(),
                    'query_string': changelist.get_query_string(*self.get_query_params(plus_lookup)),
                },
                'minus': {
                    'selected': self.value() and minus_lookup in self.values(),
                    'query_string': changelist.get_query_string(*self.get_query_params(minus_lookup)),
                },
                'only': {
                    'selected': self.value() and lookup in values,
                    'query_string': changelist.get_query_string({self.parameter_name: plus_lookup}),
                }
            }
