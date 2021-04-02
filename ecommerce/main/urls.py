from django.urls import path
from .views import BaseView, CategoryView, ProfileView, LoginView, LogoutView, RegistrationView, CartView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('cart/', CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
