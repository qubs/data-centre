from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views


admin.site.site_header = 'QUBS Data Centre Admin'

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^climate/export/', include('climate_exporter.urls')),
    url(r'^climate/manage/', include('climate_manager.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
]

# If in debug mode, serve static files from Django.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
