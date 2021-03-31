from django.shortcuts import render
from django.views import View
from .models import Category


class BaseView(View):

    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'page_role': 'goods',
        }
        return render(request, 'base.html', context=context)


class CategoryView(View):
    model = Category

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        context = {
            'category': category,
            'categories': Category.objects.all(),
            'page_role': 'goods',
        }
        return render(request, 'category.html', context=context)


class ProfileView(View):
    pass


class LoginView(View):
    pass


class LogoutView(View):
    next_page = None
    pass


class RegistrationView(View):
    pass


class CartView(View):
    pass
