import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.test import Client, TestCase
from django.urls import reverse
from django import forms


User = get_user_model()


class UserViewsTests(TestCase):
    TOKEN_GENERATOR = PasswordResetTokenGenerator()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        user_b64 = base64.b64encode(f'{cls.user,id}'.encode())
        user_b64_str = user_b64.decode('ascii')
        cls.user_b64 = (
            user_b64_str[:-2]
            if user_b64_str[-2:] == "=="
            else user_b64_str
        )
        cls.token = cls.TOKEN_GENERATOR.make_token(cls.user)

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_pages_names = {
            reverse('users:login'): 'users/login.html',
            reverse('users:signup'): 'users/signup.html',
            reverse('users:password_change'):
                'users/password_change_form.html',
            reverse('users:password_change_done'):
                'users/password_change_done.html',
            reverse('users:password_reset'):
                'users/password_reset_form.html',
            reverse('users:password_reset_done'):
                'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': self.user_b64, 'token': self.token}
            ): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
                'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }

        for url, template in templates_pages_names.items():
            response = self.authorized_client.get(url)
            self.assertTemplateUsed(response, template)

    def test_sugnup_use_correct_context(self):
        """Шаблон signup сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': UsernameField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
