from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView

from .forms import UserForm, LoginForm, ItemCreateForm
from .models import Category, Item, Article, Customer, Vendor
from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic.edit import CreateView, UpdateView

User = get_user_model()


class BaseView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'main/base.html', context=context)


class ItemView(View):
    context_object_name = 'item'
    template_name = 'main/item_detail.html'

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
    template_name = 'main/category.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        context['category'] = category
        return context

    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        object_list = Item.objects.filter(Q(category=category) | Q(category__parent=category))

        return object_list


class ItemListView(ListView):
    model = Item
    template_name = 'main/item_list.html'
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
    template_name = 'main/article_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class LoginView(View):
    template_name = 'main/login.html'

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
                return HttpResponseRedirect('/profile/')
            else:
                return HttpResponseRedirect('/login/')

        context = {
            'form': form,
            'page_role': 'login',
        }
        return render(request, self.template_name, context)


class ItemCreate(CreateView):
    template_name = 'main/item_form.html'
    model = Item
    fields = ['title', 'category', 'color', 'image', 'description', 'price', 'tag', 'slug',]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        vendor = Vendor.objects.get(user=user)
        form = ItemCreateForm(request.POST)

        if form.is_valid():
            item = self.model.objects.create(vendor=vendor)
            item.slug = form.cleaned_data['slug']
            item.image = form.cleaned_data['slug']

            return HttpResponseRedirect(f'/vendor/item_update/{item.slug}/')
        else:
            messages.add_message(request, messages.ERROR, form.errors)

        context = {
            'form': form,
            'page_role': 'item',
        }
        return render(request, self.template_name, context)


class ItemUpdate(UpdateView):
    model = Item
    fields = ['title', 'category', 'tag', 'color', 'image', 'description', 'price', 'slug',]
    template_name_suffix = '_update_form'


class RegistrationView(View):
    """ Форма регистрации нового пользоваетля - клиента"""
    pass


class CartView(View):
    """ Представление для корзины с товарами """
    pass


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Customer
    context_object_name = 'profile'
    template_name = 'main/account_profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.login_url)

        user = request.user
        if Customer.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Customer, fields=('birthday',))
        if Vendor.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Vendor, fields=('name', 'phone', 'address',))

        form = UserForm(instance=user)
        formset = FormSet(instance=user)

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
        if Customer.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Customer, fields=('birthday',))
            profile = Customer.objects.get(user=user)
            fields = ['birthday']
        elif Vendor.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Vendor, fields=('name', 'phone', 'address',))
            profile = Vendor.objects.get(user=user)
            fields = ['name', 'address', 'phone']
        else:
            return HttpResponseRedirect('/login/')

        form = UserForm(request.POST, instance=user)  # Иначе это будет новый экземпляр с попыткой создать нового юзера
        formset = FormSet(request.POST, instance=user)  # Иначе formset не привяжется к экземпляру

        if form.is_valid():
            for field in ['first_name', 'last_name', 'username', 'email']:
                vars(user)[field] = form.cleaned_data[field]
            user.save()
        else:
            messages.add_message(request, messages.ERROR, form.errors['username'])

        if formset.is_valid():
            if formset.cleaned_data[0]['DELETE']:
                user.delete()
                profile.delete()
            else:
                for field in fields:
                    vars(profile)[field] = formset.cleaned_data[0][field]

            profile.save()

        else:
            messages.add_message(request, messages.ERROR, formset.errors[0])

        return HttpResponseRedirect('/profile/')

