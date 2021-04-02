from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('about/<str:slug>/', views.ArticleView.as_view(), name='article'),
    path('item/<str:slug>/', views.ItemView.as_view(), name='item'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('category/<str:slug>/', views.CategoryItemsView.as_view(), name='category'),
    path('account/profile/', views.CustomerView.as_view(), name='profile'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(next_page="/account/profile/"), name='logout'),
    path('account/registration/', views.RegistrationView.as_view(), name='registration'),
    path('vendor/profile/', views.VendorView.as_view(), name='vendor'),
    path('cart/', views.CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
