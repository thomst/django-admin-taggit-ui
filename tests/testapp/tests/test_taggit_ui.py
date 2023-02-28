

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlencode
from taggit.models import Tag
from testapp.models import ModelA
from testapp.models import ModelB
from testapp.management.commands.createtestdata import create_test_data


class TaggitUiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.url = reverse('admin:testapp_modela_changelist')

    def test_01_filtering(self):
        queries = (
            ('', 36),
            (urlencode({'tags': '+one'}), 36),
            (urlencode({'tags': '+one,-two'}), 18),
            (urlencode({'tags': '+one,-three'}), 24),
            (urlencode({'tags': '+one,-two,-three'}), 6),
            (urlencode({'tags': '+two,+three'}), 30),
            (urlencode({'tags': '-two,+three'}), 12),
        )
        for query, count in queries:
            resp = self.client.get(self.url + '?' + query)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('{} selected'.format(count), resp.content.decode('utf8'))

    def test_02_action(self):
        # Render action form.
        ids = [i for i in range(1,7)]
        post_data = dict()
        post_data['action'] = 'manage_tags'
        post_data['_selected_action'] = ids

        resp = self.client.post(self.url, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<h1>Manage Tags</h1>')

        # Add tags.
        tags = ['test1', 'test2']
        tag1, tag2 = tags
        post_data = dict()
        post_data['action'] = 'manage_tags'
        post_data['tags'] = ' '.join(tags)
        post_data['root'] = True
        post_data['add'] = 'Add'
        post_data['_selected_action'] = ids

        resp = self.client.post(self.url, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)

        objs_by_tag1 = ModelA.objects.filter(tags__name__in=[tag1])
        objs_by_tag2 = ModelA.objects.filter(tags__name__in=[tag2])
        objs_by_id = ModelA.objects.filter(id__in=ids)
        self.assertEqual(len(objs_by_tag1), 6)
        self.assertEqual(set(objs_by_tag1), set(objs_by_id))
        self.assertEqual(set(objs_by_tag2), set(objs_by_id))

        # Remove tags.
        objs_by_three = ModelA.objects.filter(tags__name__in=['three'])
        ids = [o.id for o in objs_by_three]
        post_data = dict()
        post_data['action'] = 'manage_tags'
        post_data['tags'] = ','.join(tags)
        post_data['root'] = True
        post_data['remove'] = 'Remove'
        post_data['_selected_action'] = ids

        resp = self.client.post(self.url, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag1])
        self.assertEqual(len(objs_by_tag), 4)

    def test_02_api(self):
        # Delete tag.
        tag1 = Tag.objects.get(name='one')
        url = reverse('remove-tag', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag1.name])
        self.assertEqual(len(objs_by_tag), 0)
        self.assertFalse(objs_by_tag)
        self.assertRaises(Tag.DoesNotExist, Tag.objects.get, pk=tag1.id)

        # Remove tag that's linked with objects of two different models.
        tag2 = Tag.objects.get(name='two')
        ModelB.objects.get(pk=1).tags.add(tag2.name)
        url = reverse('remove-tag', kwargs=dict(tag_id=tag2.id, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag2.name])
        self.assertEqual(len(objs_by_tag), 0)
        self.assertFalse(objs_by_tag)
        self.assertTrue(Tag.objects.get(pk=tag2.id))
        self.assertTrue(Tag.objects.get(pk=tag2.id))

        # Unkown tag-id.
        url = reverse('remove-tag', kwargs=dict(tag_id=1234, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 404)

        # Unkown model.
        url = reverse('remove-tag', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='dummy'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 404)
