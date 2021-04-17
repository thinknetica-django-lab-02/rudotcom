
from django.contrib import admin
from django.urls import path, include

from main.views import FeedbackView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
]
