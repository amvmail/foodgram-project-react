from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

handler404 = 'core.views.page_not_found'
handler403 = "core.views.permission_denied"
handler500 = "core.views.server_error"

urlpatterns = [
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipe.urls', namespace="recipe")),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
]

# if settings.DEBUG:
#    import debug_toolbar
#
#    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
#    urlpatterns += static(
#        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
#    )
