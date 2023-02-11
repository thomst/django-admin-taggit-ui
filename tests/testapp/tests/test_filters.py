

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlencode
from testapp.management.commands.createtestdata import create_test_data


class FilterTest(TestCase):
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
