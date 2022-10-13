from django.conf import settings
from django.conf.urls.static import static  # , re_path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RecipesViewSet, IngredientViewSet, TagViewSet,
                    UsersViewSet, AmountViewSet)

# from rest_framework import permissions
app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tags')
router.register('amounts', AmountViewSet, basename='amounts')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
