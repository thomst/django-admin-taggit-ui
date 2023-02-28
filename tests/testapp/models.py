# -*- coding: utf-8 -*-

from django.db import models
from taggit.managers import TaggableManager


class BaseModel(models.Model):
    def __str__(self):
        model_name = type(self)._meta.object_name
        return '{} [{}]'.format(model_name, self.id)

    class Meta:
        abstract = True


class ModelA(BaseModel):
    id = models.AutoField(primary_key=True)
    model_b = models.ForeignKey('ModelB', blank=True, null=True, on_delete=models.SET_NULL)
    tags = TaggableManager(blank=True)


class ModelB(BaseModel):
    id = models.AutoField(primary_key=True)
    tags = TaggableManager(blank=True)
