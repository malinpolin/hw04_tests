from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post


User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        Post.objects.create(
            text='Старый пост',
            author=cls.user
        )
        cls.form = PostForm()

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        new_post = Post.objects.last()
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': new_post.author.username},
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=new_post.text,
                id=new_post.id,
                author=new_post.author,
            ).exists()
        )

    def test_post_edit(self):
        """Валидная форма редактирует запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Отредактированный пост'
        }
        last_post = Post.objects.last()
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': last_post.id}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': last_post.id},
            )
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                id=last_post.id,
                author=last_post.author,
            ).exists()
        )

    def test_post_text_help_text(self):
        text_help_text = self.form.fields['text'].help_text
        self.assertEqual(text_help_text, 'Текст нового поста')
