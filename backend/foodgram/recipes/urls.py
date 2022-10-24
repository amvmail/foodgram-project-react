from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipe', RecipeViewSet)

urlpatterns = [
    path(
        'api/recipe/download_shopping_cart/',
        RecipeViewSet.as_view,
        name='download_shopping_cart'
    ),
    path(
        'docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'docs/openapi-schema.yml',
        TemplateView.as_view(template_name='openapi-schema.yml'),
        name='openapi'
    ),
    path('', include(router.urls)),
]
