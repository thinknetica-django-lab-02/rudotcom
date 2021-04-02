from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView, UpdateView

from .forms import UserForm, LoginForm
from .models import Category, Item, Article, Customer
from django.contrib.auth import get_user_model, login, authenticate

User = get_user_model()


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
        items = Item.objects.filter(category=category)
        context['category'] = category
        context['items'] = items
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


class CustomerView(LoginRequiredMixin, UpdateView):
    login_url = "/account/login/"
    model = Customer
    context_object_name = 'profile'
    template_name = 'main/account_profile.html'
    CustomerFormSet = inlineformset_factory(User, Customer, fields=('birthday',))

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.login_url)

        user = request.user
        form = UserForm(instance=user)
        formset = self.CustomerFormSet(instance=user)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'formset': formset,
                'page_role': 'profile',
            }
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.login_url)

        user = User.objects.get(username=request.user.username)
        form = UserForm(request.POST, instance=user)  # Иначе это будет новый экземпляр с попыткой создать нового юзера
        formset = self.CustomerFormSet(request.POST, instance=user)  # Иначе formset не привяжется к экземпляру

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
        else:
            messages.add_message(request, messages.ERROR, form.errors['username'])

        if formset.is_valid():
            customer = Customer.objects.get(user=user)
            if formset.cleaned_data[0]['DELETE']:
                user.delete()
                customer.delete()
            else:
                customer.birthday = formset.cleaned_data[0]['birthday']
                customer.save()

        else:
            messages.add_message(request, messages.ERROR, formset.errors[0])

        return HttpResponseRedirect('/account/profile/')


class LoginView(View):
    template_name = 'main/account_login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'page_role': 'login',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/account/profile/')

        context = {
            'form': form,
            'page_role': 'login',
        }
        return render(request, self.template_name, context)


class RegistrationView(View):
    """ Форма регистрации нового пользоваетля - клиента"""
    pass


class CartView(View):
    """ Представление для корзины с товарами """
    pass
