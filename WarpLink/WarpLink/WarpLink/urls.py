from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vpn_auth/', include('vpn_auth.urls')),
    path('home/', include('homepage.urls')),
    path('download/', include('conf_generator.urls')),
    path('', RedirectView.as_view(url='/vpn_auth/login/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
