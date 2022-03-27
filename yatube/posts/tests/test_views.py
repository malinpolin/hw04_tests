from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group


User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username='TestUser1')
        cls.user_2 = User.objects.create_user(username='TestUser2')
        cls.group_one = Group.objects.create(
            title='Тестовая группа_1',
            slug='test_slug_1',
            description='Тестовое описание',
        )
        cls.group_two = Group.objects.create(
            title='Тестовая группа_2',
            slug='test_slug_2',
            description='Тестовое описание',
        )
        # Только не плачь, пожалуйста, над моим кодом)
        # Всего 36 постов, из них:
        # - по 18 постов у user_1 и user_2
        # - по 12 постов в группе 1, в группе 2, без группы
        cls.post_1 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_2 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_3 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_4 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_5 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_6 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_7 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост без группы',
        )
        cls.post_8 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_9 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_10 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_11 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_12 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост без группы',
        )
        cls.post_13 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_14 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_15 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_16 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_17 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост без группы',
        )
        cls.post_18 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_19 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_20 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_21 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_22 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_23 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_24 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_25 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост без группы',
        )
        cls.post_26 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_27 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_28 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_29 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_30 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_31 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_32 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 1',
            group=cls.group_one,
        )
        cls.post_33 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост без группы',
        )
        cls.post_34 = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )
        cls.post_35 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост без группы',
        )
        cls.post_36 = Post.objects.create(
            author=cls.user_2,
            text='Тестовый пост с группой 2',
            group=cls.group_two,
        )

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
        url_arg={}
    ):
        """На каждой странице переданного URL требуемое кол-во постов"""
        paginator_count = 10
        page_ten_count = expected_count // paginator_count
        page_count = (
            expected_count // paginator_count + 1
            if expected_count % paginator_count > 0
            else expected_count // paginator_count
        )
        while page_ten_count > 0:
            response = self.authorized_client.get(
                reverse(url, kwargs=url_arg) + f'?page={page_ten_count}'
            )
            self.assertEqual(
                len(response.context['page_obj']),
                paginator_count,
            )
            page_ten_count -= 1
        else:
            if page_count > page_ten_count:
                response = self.authorized_client.get(
                    reverse(url, kwargs=url_arg) + f'?page={page_count}'
                )
                self.assertEqual(
                    len(response.context['page_obj']),
                    expected_count % 10,
                )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_one.slug},
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user_1.username},
            ): 'posts/profile.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post_1.id},
            ): 'posts/create_post.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post_2.id},
            ): 'posts/post_detail.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
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
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_one.slug},
            )
        )
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
        url_arg = {'slug': self.group_one.slug}
        self.check_pages_contains_correct_count_records(
            url,
            expected_count,
            url_arg
        )

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post_1.id},
            )
        )
        self.assertEqual(
            response.context.get('post').author.id,
            self.post_1.author.id
        )
        self.assertEqual(
            response.context.get('post').text,
            self.post_1.text
        )
        post_count = Post.objects.filter(
            author=self.post_1.author
        ).count()
        self.assertEqual(response.context.get('post_count'), post_count)
        self.assertEqual(
            response.context.get('title'),
            'Пост ' + self.post_1.text[:30]
        )

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.user_1.username},
            )
        )
        expected_first_object = Post.objects.filter(
            author=self.user_1
        ).latest('pub_date')
        self.check_context_for_list_pages(
            response.context,
            expected_first_object
        )
        post_count = Post.objects.filter(
            author=self.user_1
        ).count()
        self.assertEqual(response.context.get('post_count'), post_count)
        self.assertEqual(
            response.context.get('title'),
            'Профайл пользователя ' + self.user_1.username
        )

    def test_profile_pages_pages_contains_correct_count_records(self):
        """На страницы profile передаётся ожидаемое количество объектов"""
        url = 'posts:profile'
        expected_count = Post.objects.filter(author=self.user_1).count()
        url_arg = {'username': self.user_1.username}
        self.check_pages_contains_correct_count_records(
            url,
            expected_count,
            url_arg
        )

    def test_create_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
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
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post_6.id},
            )
        )
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
            self.post_6.id
        )
        self.assertEqual(response.context.get('title'), 'Редактировать пост')
        self.assertTrue(response.context.get('is_edit'))

    def test_new_post(self):
        """Проверка нового поста"""
        post_37 = Post.objects.create(
            author=self.user_2,
            text='Новый пост с группой 2',
            group=self.group_two,
        )
        reverse_names_correct_pages = (
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': post_37.group.slug},
            ),
            reverse(
                'posts:profile',
                kwargs={'username': post_37.author.username},
            )
        )
        for reverse_name in reverse_names_correct_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertIn(post_37, response.context['page_obj'])
        reverse_names_incorrect_pages = (
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_one.slug},
            ),
            reverse(
                'posts:profile',
                kwargs={'username': self.user_1.username},
            )
        )
        for reverse_name in reverse_names_incorrect_pages:
            response = self.authorized_client.get(reverse_name)
            self.assertNotIn(post_37, response.context['page_obj'])
