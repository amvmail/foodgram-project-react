from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from recipe.recipe_global import QUANT_OF_POSTS
from .forms import RecipeForm, CommentForm
from .models import Tag, Recipe, User, Comment, Follow


def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функции первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')

    return check_user


def index(request):
    template = 'recipe/index.html'
    recipe = Recipe.objects.all()
    # убрал_.order_by('-pub_date')_
    paginator = Paginator(recipe, QUANT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'recipe': recipe,
        'page_obj': page_obj,

    }
    return render(request, template, context)


def tag_recipe(request, slug):
    template = 'recipe/tag_list.html'
    tag = get_object_or_404(Tag, slug=slug)
    recipe = Recipe.objects.all().filter(tag=tag)
    paginator = Paginator(recipe, QUANT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'tag': tag,
        'recipe': recipe,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Здесь код запроса к модели и создание словаря контекста
def profile(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    recipe = author.recipe.all()
    paginator = Paginator(recipe, QUANT_OF_POSTS)
    template = 'recipe/profile.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = False
    if user.is_authenticated:
        check_follower = Follow.objects.filter(user=user, author=author)
        if check_follower.exists():
            following = True
    context = {
        'author': author,
        'recipe': recipe,  # Проверить - переделать recipe
        'page_obj': page_obj,
        'user': user,
        'following': following,
    }
    return render(request, template, context)


def recipe_detail(request, recipe_id):
    detail_recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_count = Recipe.objects.filter(author=detail_recipe.author).count()
    template = 'recipe/recipe_detail.html'
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(recipe=detail_recipe)
    context = {
        'post_count': post_count,
        'detail_recipe': detail_recipe,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


@login_required
def recipe_create(request):
    template = 'recipe/create_recipe.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        form.save()
        return redirect('recipe:profile', username=request.user)
    return render(request, template, {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    is_edit = True
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipe:recipe_detail', recipe_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=recipe)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('recipe:recipe_detail', recipe_id=recipe_id)
    context = {
        'form': form,
        'recipe_id': recipe_id,
        'recipe': recipe,
        'is_edit': is_edit,
    }
    return render(request, 'recipe/create_recipe.html', context)


@login_required
def add_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.recipe = recipe
        comment.save()
    return redirect('recipe:recipe_detail', recipe_id=recipe_id)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    template = 'recipe/follow.html'
    user = request.user
    author = get_object_or_404(User, username=user)
    recipe = Recipe.objects.filter(author__following__user=request.user)
    # posts = Post.objects.filter(user=request.user)
    paginator = Paginator(recipe, QUANT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'recipe': recipe,
        'author': author,
        'user': user,
        'page_obj': page_obj,
    }
    # context = get_page_context(posts, request)
    return render(request, template, context, page_obj)


@login_required
def profile_follow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('recipe:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user,
        author=author
    )
    follow.delete()
    return redirect('recipe:profile', username)
