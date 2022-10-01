from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipesViewSet, basename='recipes')
#router_v1.register(r'recipes/(?P<post_id>\d+)/subscribe',
#                   SubscriptionViewSet, basename='subscribe')
# router_v1.register('groups', GroupViewSet, basename='group')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
#    path('v1/follow/', APIFollowList.as_view()),
#    path('v1/follow/<pk>', APIFollowList.as_view()),
    path(
        'docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
