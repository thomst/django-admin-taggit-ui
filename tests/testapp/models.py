# -*- coding: utf-8 -*-

from django.db import models
from taggit.managers import TaggableManager


class ModelA(models.Model):
    id = models.AutoField(primary_key=True)
    model_b = models.ForeignKey('ModelB', blank=True, null=True, on_delete=models.SET_NULL)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return 'ModelA {}'.format(self.id)


class ModelB(models.Model):
    id = models.AutoField(primary_key=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return 'ModelB {}'.format(self.id)
