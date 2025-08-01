from django.contrib import admin
from django.urls import path, include
# <-- ДОБАВЛЯЕМ ИМПОРТЫ -->
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# <-- ДОБАВЛЯЕМ СТРОКУ ДЛЯ МЕДИАФАЙЛОВ -->
# Это нужно только в режиме разработки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

