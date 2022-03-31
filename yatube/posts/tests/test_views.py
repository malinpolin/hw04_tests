from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group, User
from posts.tests import test_constant as const


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username=const.USERNAME_1)
        cls.user_2 = User.objects.create_user(username=const.USERNAME_2)
        cls.group_one = Group.objects.create(
            title=const.GROUP_TITLE_1,
            slug=const.GROUP_SLUG_1,
            description=const.GROUP_DESCRIPTION,
        )
        cls.group_two = Group.objects.create(
            title=const.GROUP_TITLE_2,
            slug=const.GROUP_SLUG_2,
            description=const.GROUP_DESCRIPTION,
        )
        posts_count = 36
        cls.create_test_base(cls, posts_count)
        cls.post = Post.objects.filter(
            author=cls.user_1,
            group=cls.group_one
        ).first()
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail',
            kwargs={'post_id': cls.post.id}
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit',
            kwargs={'post_id': cls.post.id}
        )

    def create_test_base(self, posts_count):
        posts_list = []
        for i in range(1, (posts_count // 2) + 1):
            if i % 3 == 0:
                posts_list.append(
                    Post(
                        author=self.user_1,
                        text='Тестовый пост без группы'
                    )
                )
                posts_list.append(
                    Post(
                        author=self.user_2,
                        text='Тестовый пост без группы'
                    )
                )
            elif i % 2 == 0:
                posts_list.append(
                    Post(
                        author=self.user_1,
                        group=self.group_two,
                        text='Тестовый пост группы 2'
                    )
                )
                posts_list.append(
                    Post(
                        author=self.user_2,
                        group=self.group_two,
                        text='Тестовый пост группы 2'
                    )
                )
            else:
                posts_list.append(
                    Post(
                        author=self.user_1,
                        group=self.group_one,
                        text='Тестовый пост группы 1'
                    )
                )
                posts_list.append(
                    Post(
                        author=self.user_2,
                        group=self.group_one,
                        text='Тестовый пост группы 1'
                    )
                )
        Post.objects.bulk_create(posts_list)

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_1)

    def check_context_for_list_pages(self, context, expected):
        """Проверка контекста для страниц index, group_list и profile"""
        first_object = context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_id_0 = first_object.id
        self.assertEqual(post_text_0, expected.text)
        self.assertEqual(post_author_0.id, expected.author.id)
        self.assertEqual(post_id_0, expected.id)
        if first_object.group:
            post_group_0 = first_object.group
            self.assertEqual(post_group_0.slug, expected.group.slug)
            self.assertEqual(post_group_0.id, expected.group.id)
            self.assertEqual(
                post_group_0.description,
                expected.group.description
            )

    def check_pages_contains_correct_count_records(
        self,
        url,
        expected_count,
        url_kwargs={}
    ):
        """На каждой странице переданного URL требуемое кол-во постов"""
        paginator_count = settings.PAGINATOR_COUNT
        page_ten_count = expected_count // paginator_count
        page_count = (
            expected_count // paginator_count + 1
            if expected_count % paginator_count > 0
            else expected_count // paginator_count
        )
        while page_ten_count > 0:
            response = self.authorized_client.get(
                reverse(url, kwargs=url_kwargs) + f'?page={page_ten_count}'
            )
            self.assertEqual(
                len(response.context['page_obj']),
                paginator_count,
            )
            page_ten_count -= 1
        else:
            if page_count > page_ten_count:
                response = self.authorized_client.get(
                    reverse(url, kwargs=url_kwargs) + f'?page={page_count}'
                )
                self.assertEqual(
                    len(response.context['page_obj']),
                    expected_count % paginator_count,
                )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            const.INDEX_URL: const.INDEX_TEMPLATE,
            const.POST_CREATE_URL: const.POST_CREATE_TEMPLATE,
            const.GROUP_LIST_URL: const.GROUP_LIST_TEMPLATE,
            const.PROFILE_URL: const.PROFILE_TEMPLATE,
            self.POST_EDIT_URL: const.POST_EDIT_TEMPLATE,
            self.POST_DETAIL_URL: const.POST_DETAIL_TEMPLATE,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.INDEX_URL)
        expected_first_object = Post.objects.latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('title'),
            'Последние обновления на сайте'
        )

    def test_index_pages_contains_correct_count_records(self):
        """На страницы index передаётся ожидаемое количество объектов"""
        expected_count = Post.objects.count()
        url = 'posts:index'
        self.check_pages_contains_correct_count_records(url, expected_count)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.GROUP_LIST_URL)
        expected_first_object = Post.objects.filter(
            group=self.group_one
        ).latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('group').id,
            expected_first_object.group.id
        )

    def test_group_list_pages_contains_correct_count_records(self):
        """На страницы group_list передаётся ожидаемое количество объектов"""
        url = 'posts:group_list'
        expected_count = Post.objects.filter(group=self.group_one).count()
        url_kwargs = {'slug': self.group_one.slug}
        self.check_pages_contains_correct_count_records(
            url,
            expected_count,
            url_kwargs
        )

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_DETAIL_URL)
        self.assertEqual(
            response.context.get('post').author.id,
            self.post.author.id
        )
        self.assertEqual(
            response.context.get('post').text,
            self.post.text
        )
        self.assertEqual(
            response.context.get('title'),
            'Пост ' + self.post.text[:30]
        )

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.PROFILE_URL)
        expected_first_object = Post.objects.filter(
            author=self.user_1
        ).latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        self.assertEqual(
            response.context.get('title'),
            'Профайл пользователя ' + self.user_1.username
        )

    def test_profile_pages_pages_contains_correct_count_records(self):
        """На страницы profile передаётся ожидаемое количество объектов"""
        url = 'posts:profile'
        expected_count = Post.objects.filter(author=self.user_1).count()
        url_kwargs = {'username': self.user_1.username}
        self.check_pages_contains_correct_count_records(
            url,
            expected_count,
            url_kwargs
        )

    def test_create_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.POST_CREATE_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context.get('title'), 'Новый пост')

    def test_edit_show_correct_context(self):
        """Шаблон edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_EDIT_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(
            response.context.get('post').id,
            self.post.id
        )
        self.assertEqual(response.context.get('title'), 'Редактировать пост')
        self.assertTrue(response.context.get('is_edit'))

    def test_new_post(self):
        """Проверка нового поста"""
        new_post = Post.objects.create(
            author=self.user_1,
            text='Новый пост в группе 2',
            group=self.group_two,
        )
        reverse_names_correct_pages = (
            const.INDEX_URL,
            reverse(
                'posts:group_list',
                kwargs={'slug': new_post.group.slug},
            ),
            const.PROFILE_URL,
        )
        for reverse_name in reverse_names_correct_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertIn(new_post, response.context['page_obj'])
        reverse_names_incorrect_pages = (
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_one.slug},
            ),
            reverse(
                'posts:profile',
                kwargs={'username': self.user_2.username},
            )
        )
        for reverse_name in reverse_names_incorrect_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertNotIn(new_post, response.context['page_obj'])
