from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        RecipeViewSet.as_view,
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
]
