from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView

from .forms import UserForm, LoginForm, ItemUpdateForm, FeedbackForm
from .models import Category, Item, Article, Customer, Vendor
from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView
from .forms import FeedbackForm

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

        # Является ли user владельцем товара (для ссылки на редактирование)
        is_owned = item.vendor.user == request.user

        context = {
            'category': category,
            'item': item,
            'is_owned': is_owned,
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
        context['active_tag'] = tag
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


class LoginView(LoginView):
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
        next_page = request.GET.get('next') or '/profile/'

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponseRedirect('/login/')

        context = {
            'form': form,
            'page_role': 'login',
        }
        return render(request, self.template_name, context)


class ItemCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = ItemUpdateForm
    template_name = 'main/item_form.html'
    permission_required = ['main.add_item', 'main.view_item']

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        vendor = Vendor.objects.get(user=user)
        item = Item(vendor=vendor)
        form = ItemUpdateForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return HttpResponseRedirect(f'/item/{item.slug}/')
        else:
            messages.add_message(request, messages.ERROR, form.errors)

        context = {
            'form': form,
            'page_role': 'item',
        }
        return render(request, self.template_name, context)


class ItemUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Item
    form_class = ItemUpdateForm
    template_name_suffix = '_update_form'
    permission_required = ('main.change_item', 'main.delete_item', 'main.view_item')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(slug=self.kwargs['slug'])
        context['image_thumb'] = item.image_thumb
        return context


class SignUpView(CreateView):
    model = Customer
    form_class = UserForm
    template_name = 'main/sign_up.html'


class CartView(View):
    """ Представление для корзины с товарами """
    pass


class FeedbackView(FormView):
    template_name = 'ecommerce/contact.html'
    form_class = FeedbackForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Customer
    context_object_name = 'profile'
    template_name = 'main/profile.html'

    def get(self, request, *args, **kwargs):

        user = request.user
        formset = ''
        # Создаем доп поля формы для Customer
        is_vendor = False
        if Vendor.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Vendor,
                                            fields=('name', 'phone', 'address', 'image',))
            formset = FormSet()
            is_vendor = True

        return render(
            request,
            self.template_name,
            {
                'form': UserForm(instance=user),
                'formset': formset,
                'page_role': 'profile',
                'is_vendor': is_vendor,
            }
        )

    def post(self, request, *args, **kwargs):

        user = User.objects.get(username=request.user.username)
        formset = None
        if Customer.objects.filter(user=user).count():
            profile = Customer.objects.get(user=user)
        elif Vendor.objects.filter(user=user).count():
            FormSet = inlineformset_factory(User, Vendor, fields=('name', 'phone', 'address', 'image',))
            formset = FormSet(request.POST, request.FILES, instance=user)  # Иначе formset не привяжется к экземпляру
            profile = Vendor.objects.get(user=user)
            fields = ['name', 'address', 'phone', 'image']
        else:
            return HttpResponseRedirect('/login/')

        form = UserForm(request.POST, request.FILES, instance=user)
        # Иначе это будет новый экземпляр с попыткой создать нового юзера

        if form.is_valid():
            for field in ['first_name', 'last_name', 'username', 'email']:
                vars(user)[field] = form.cleaned_data[field]
            user.save()
        else:
            messages.add_message(request, messages.ERROR, form.errors['username'])

        if formset:
            if formset.is_valid():
                print(formset)
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
