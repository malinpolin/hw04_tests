import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    post_list = group.group_name.all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    title = f'Профайл пользователя {username}'
    context = {
        'author': author,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    title = 'Пост ' + post.text[0:30]
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'title': title,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.pub_date = datetime.datetime.today()
        post.save()
        return redirect(f'/profile/{request.user.username}/')
    form = PostForm()
    template = 'posts/create_post.html'
    title = 'Новый пост'
    context = {
        'form': form,
        'title': title,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect(f'/posts/{post_id}')
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(f'/posts/{post_id}')
    form = PostForm(instance=post)
    template = 'posts/create_post.html'
    title = 'Редактировать пост'
    context = {
        'form': form,
        'title': title,
        'post': post,
        'is_edit': True,
    }
    return render(request, template, context)
