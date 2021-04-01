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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        context['category'] = category
        return context


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        return context

    def get_queryset(self):
        query = self.request.GET.get('tag')
        object_list = Item.objects.filter(tag__string=query)

        return object_list


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
