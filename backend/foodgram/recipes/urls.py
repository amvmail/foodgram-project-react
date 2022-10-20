from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       download_shopping_cart)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
]
