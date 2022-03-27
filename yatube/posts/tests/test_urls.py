from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='PostAuthor')
        cls.user = User.objects.create_user(username='NotPostAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовый пост',
        )

    def setUp(self):
        # Создаём неавторизованного клиента
        self.guest_client = Client()
        # Создаем авторизованного клиента - автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user_author)
        # Создаем авторизованного клиента - не автора поста
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_url_for_unauthorized_user(self):
        """Проверяем доступность страниц для любого пользователя"""
        url_names = (
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.id}/'
        )
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unknown_page_for_unauthorized_user(self):
        """Запрос к несуществующей странице для любого пользователя"""
        url = '/unknown_page/'
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_url_for_authorized_user(self):
        """Доступность /create/ для авторизованного пользователя"""
        url = '/create/'
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_url_for_author(self):
        """Проверяем доступность страницы /posts/edit/ для автора"""
        url = f'/posts/{self.post.id}/edit/'
        response = self.authorized_client_author.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя"""
        url = '/create/'
        response = self.guest_client.get(url, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_edit_url_redirect_not_author(self):
        """Страница /posts/post.id/edit/ перенаправляет
        авторизованного пользователя - не автора.
        """
        url = f'/posts/{self.post.id}/edit/'
        response = self.authorized_client.get(url, follow=True)
        self.assertRedirects(response, f'/posts/{self.post.id}/')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url)
                self.assertTemplateUsed(response, template)
