from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),

]
