# -*- coding: utf-8 -*-

from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag
from taggit.models import TaggedItem


class CanDeleteTag(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('taggit.delete_tag')


class RemoveTagApi(APIView):
    permission_classes = [IsAuthenticated, CanDeleteTag]

    def delete(self, request, app_label=None, model_name=None, tag_id=None):
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            raise Http404('Tag not found: {}'.format(tag_id))

        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            raise Http404('Model not found: {}.{}'.format(app_label, model_name))

        TaggedItem.objects.filter(content_type=content_type, tag=tag).delete()

        # Cleanup tag if no tagged-items left.
        if not TaggedItem.objects.filter(tag=tag):
            tag.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
