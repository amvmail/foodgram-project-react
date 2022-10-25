from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls)),
]
