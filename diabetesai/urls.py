"""
URL configuration for diabetesai project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from predictor import views as predictor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', predictor_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('predictor/', include('predictor.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)