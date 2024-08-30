from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    # path('accounts/', include('allauth.urls')),  # new
    path('dashboard/', include('dashboard.urls')),


    path('ckeditor5/', include('django_ckeditor_5.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    # Serve media files in production (not recommended)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
handler404 = 'base.views.not_found'
