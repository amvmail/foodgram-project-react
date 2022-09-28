from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler400 = 'foodgram.views.bad_request'  # noqa
handler403 = 'foodgram.views.permissions_denied'  # noqa
handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('about/',
         include('about.urls', namespace='about')),
    path('admin/',
         admin.site.urls),
    path('auth/',
         include('users.urls')),
    path('',
         include('recipes.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
