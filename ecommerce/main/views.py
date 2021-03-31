import datetime

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, View
from .models import Category, Item


class BaseView(View):

    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'page_role': 'goods',
        }
        return render(request, 'base.html', context=context)


class ItemView(View):
    model = Item
    context_object_name = 'item'
    template_name = 'item_detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        item = Item.objects.get(slug=slug)
        category = item.category
        context = {
            'category': category,
            'categories': Category.objects.all(),
            'item': item,
        }
        return render(request, self.template_name, context=context)


class CategoryItemsView(ListView):

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        items = Item.objects.filter(Q(category=category) | Q(category__parent=category))
        context = {
            'category': category,
            'categories': Category.objects.all(),
            'page_role': 'goods',
            'items': items,
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
