from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('item/<str:slug>/', views.ItemView.as_view(), name='item'),
    path('category/<str:slug>/', views.CategoryItemsView.as_view(), name='category'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('cart/', views.CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
