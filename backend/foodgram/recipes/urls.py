from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe,
         name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe,
         name='delete_recipe'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('favorites/', views.favorites, name='favorites'),
    path('change_favorites/<int:recipe_id>/', views.change_favorites,
         name='change_favorites'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/', views.following, name='follow'),
    path('subscriptions/<int:author_id>/', views.subscriptions,
         name='subscriptions'),
    path('purchases/', views.get_purchases, name='get_purchases'),
    path('purchases/<int:recipe_id>/', views.purchases, name='purchases'),
    path('shoplist/', views.shoplist, name='shoplist'),
]
