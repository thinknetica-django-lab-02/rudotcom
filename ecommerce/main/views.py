import datetime

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from .models import Category, Item, Article


class BaseView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'base.html', context=context)


class ItemView(View):
    context_object_name = 'item'
    template_name = 'item_detail.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        item = Item.objects.get(slug=slug)
        category = item.category
        context = {
            'category': category,
            'item': item,
        }
        return render(request, self.template_name, context=context)


class CategoryItemsView(ListView):
    model = Item
    template_name = 'category.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        items = Item.objects.filter(Q(category=category) | Q(category__parent=category))
        context = {
            'category': category,
            'items': items,
        }
        return render(request, self.template_name, context=context)


class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


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
