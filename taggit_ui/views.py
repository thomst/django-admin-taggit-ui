# -*- coding: utf-8 -*-

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag


class CanDeleteTag(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('taggit.delete_tag')


class DeleteTagAPI(APIView):
    permission_classes = [IsAuthenticated, CanDeleteTag]

    def delete(self, request, id=None):
        try:
            tag = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            raise Http404
        else:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
