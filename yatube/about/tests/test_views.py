from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URLs, генерируемые при помощи имен about, доступны."""
        url_names = ('about:author', 'about:tech')
        for url in url_names:
            response = self.guest_client.get(reverse(url))
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_pages_names = {
            'about:author': 'about/author.html',
            'about:tech': 'about/tech.html'
        }
        for url, template in templates_pages_names.items():
            response = self.guest_client.get(reverse(url))
            self.assertTemplateUsed(response, template)
