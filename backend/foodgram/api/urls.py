from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipesViewSet,
    IngredientViewSet,
    TagViewSet,
    UserViewSet,
    get_jwt_token,
    signup
    # SignUpViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredient', IngredientViewSet, basename='ingredient')
router.register('tag', TagViewSet, basename='tags')

router.register('users', UserViewSet)
# router.register('signup', SignUpViewSet, basename='signup')

urls_auth = [
    path('users/', signup, name='users'),
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='token'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(urls_auth)),
]
