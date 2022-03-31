from django import forms

from posts.models import Post, Group


class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        help_text='Группа, к которой будет относиться пост',
        label='Название группы',
    )

    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Текст нового поста',
        }
        labels = {
            'text': 'Текст поста',
        }
