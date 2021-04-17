from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('about/<str:slug>/', views.ArticleView.as_view(), name='article'),
    path('item/new/', views.ItemCreate.as_view(), name='item_new'),
    path('item/<str:slug>/', views.ItemView.as_view(), name='item'),
    path('item/<str:slug>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('category/<str:slug>/', views.CategoryItemsView.as_view(), name='category'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/login/"), name='logout'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('accounts/', include('allauth.urls')),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
