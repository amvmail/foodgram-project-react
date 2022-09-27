from django.urls import path

from . import views

app_name = 'recipe'

urlpatterns = [
    # начальная страница
    path('', views.index, name='index'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    # посты групп - сделать 'author/<slug:slug>/'
    # path('tag/<slug:slug>/', views.tag_recipe, name='tag_recipe'),
    # профайл user
    path('profile/<str:username>/', views.profile, name='profile'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('favorites/', views.favorites, name='favorites'),
    path('change_favorites/<int:recipe_id>/', views.change_favorites,
         name='change_favorites'),
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
    path('purchases/', views.get_purchases, name='get_purchases'),
    path('purchases/<int:recipe_id>/', views.purchases, name='purchases'),
    path('shoplist/', views.shoplist, name='shoplist'),
]
