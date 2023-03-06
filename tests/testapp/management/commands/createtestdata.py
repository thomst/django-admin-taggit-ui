# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from testapp.models import ModelA, ModelB
from testapp.models import ModelOne, ModelTwo, ModelThree, ModelFour, ModelFive


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

    # Create test-data for ModelOne serie.
    ModelOne.objects.all().delete()
    ModelTwo.objects.all().delete()
    ModelThree.objects.all().delete()
    ModelFour.objects.all().delete()
    ModelFive.objects.all().delete()
    [ModelOne(id=i).save() for i in range(4)]
    [ModelTwo(id=i).save() for i in range(8)]
    [ModelThree(id=i).save() for i in range(8)]
    [ModelFour(id=i).save() for i in range(8)]
    [ModelFive(id=i).save() for i in range(8)]

    obj_one = ModelOne.objects.get(id=3)
    obj_one.model_two.set(ModelTwo.objects.filter(id__in=range(3)))
    obj_one = ModelOne.objects.get(id=2)
    obj_one.model_two.set(ModelTwo.objects.filter(id__in=range(3,5)))

    obj_two = ModelTwo.objects.get(id=7)
    obj_two.model_one.set(ModelOne.objects.filter(id__in=range(4)))

    objs_two = ModelTwo.objects.filter(id__in=range(4,8))
    for index, obj in enumerate(objs_two):
        obj.model_three = ModelThree.objects.get(id=index%2)
        obj.save()

    for obj in ModelThree.objects.filter(id__in=range(2)):
        obj.model_five.set(ModelFive.objects.filter(id__in=range(3, 6)))

    for obj in ModelFour.objects.all():
        obj.model_three = ModelThree.objects.get(pk=obj.id)
        obj.save()


class Command(BaseCommand):
    help = 'Create test data.'

    def handle(self, *args, **options):
        create_test_data()
