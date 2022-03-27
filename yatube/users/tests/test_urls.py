from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client


User = get_user_model()


class UserURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_url_for_unauthorized_user(self):
        """Проверяем доступность страниц для любого пользователя"""
        url_names = (
            '/auth/login/',
            '/auth/logout/',
            '/auth/signup/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
        )
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_url_for_authorized_user(self):
        """Проверяем доступность страниц /password_change/
        для авторизованного пользователя.
        """
        url_names = (
            '/auth/password_change/',
            '/auth/password_change/done/',
        )
        for url in url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_url_redirect_anonymous(self):
        """Страницы /password_change/ перенаправляют анонимного
        пользователя.
        """
        prefix = '/auth/login/?next='
        url_names = (
            '/auth/password_change/',
            '/auth/password_change/done/',
        )
        for url in url_names:
            response = self.guest_client.get(url, follow=True)
            redirect_address = prefix + url
            self.assertRedirects(response, redirect_address)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'users/signup.html': '/auth/signup/',
            'users/login.html': '/auth/login/',
            'users/password_change_form.html': '/auth/password_change/',
            'users/password_change_done.html': '/auth/password_change/done/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_reset_confirm.html':
                '/auth/reset/<uidb64>/<token>/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
