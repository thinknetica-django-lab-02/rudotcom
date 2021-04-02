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
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/profile/"), name='logout'),
    path('vendor/item_create/', views.ItemCreate.as_view(), name='item_create'),
    path('vendor/item_update/<str:slug>/', views.ItemUpdate.as_view(), name='item_update'),
    path('cart/', views.CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
