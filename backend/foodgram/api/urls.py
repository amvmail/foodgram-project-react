from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipesViewSet,
    IngredientViewSet,
    TagViewSet,
    UserViewSet,
    get_jwt_token,
    SignUpViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes'),
router.register('ingredient', IngredientViewSet, basename='ingredient'),
router.register('tag', TagViewSet, basename='tags'),

router.register('users', UserViewSet, basename='users'),
router.register('signup', SignUpViewSet, basename='signup')

urls_auth = [
    path('signup/', SignUpViewSet, name='signup'),
    path('users/', UserViewSet, name='users'),
    path('token/', get_jwt_token, name='token'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
]
