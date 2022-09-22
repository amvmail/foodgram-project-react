from django.urls import path

from . import views

app_name = 'recipe'

urlpatterns = [
    # начальная страница
    path('', views.index, name='index'),
    # посты групп - сделать 'author/<slug:slug>/'
    path('tag/<slug:slug>/', views.tag_recipe, name='tag_recipe'),
    # профайл user
    path('profile/<str:username>/', views.profile, name='profile'),
    # просмотр записи
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    # создание нового поста
    path('create/', views.recipe_create, name='recipe_create'),
    # редактирование поста
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    # добавление комментария
    path('recipe/<int:recipe>/comment/',
         views.add_comment, name='add_comment'),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]
