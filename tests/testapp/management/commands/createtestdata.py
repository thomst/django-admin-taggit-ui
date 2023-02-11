# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from testapp.models import ModelA, ModelB


def create_test_data():
    try:
        User.objects.create_superuser(
            'admin',
            'admin@testapp.org',
            'adminpassword')
    except IntegrityError:
        pass

    # clear existing data
    ModelA.objects.all().delete()
    ModelB.objects.all().delete()

    for i in range(36):

        model_a = ModelA(id=i)
        model_b = ModelB(id=i)
        model_b.save()
        model_a.model_b = model_b
        model_a.save()
        model_a.tags.add('one')

        if i % 2:
            model_a.tags.add('two')
        elif i % 3:
            model_a.tags.add('three')


class Command(BaseCommand):
    help = 'Create test data.'

    def handle(self, *args, **options):
        create_test_data()
