from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from homepage.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vpn_auth/', include('vpn_auth.urls')),
    path('home/', include('homepage.urls')),
    path('', home, name='root_home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
