from django.urls import path
from .views import BaseView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

