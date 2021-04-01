from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView, UpdateView

from .forms import UserForm
from .models import Category, Item, Article, Profile
from django.contrib.auth import get_user_model

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


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = "/admin/login/?next=/account/profile/"
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/account_profile.html'
    ProfileFormSet = inlineformset_factory(User, Profile, fields=('birthday',))

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.login_url)

        user = request.user
        form = UserForm(instance=user)
        formset = self.ProfileFormSet(instance=user)

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
        formset = self.ProfileFormSet(request.POST, instance=user)  # Иначе formset не привяжется к экземпляру

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
        else:
            messages.add_message(request, messages.ERROR, form.errors['username'])

        if formset.is_valid():
            profile = Profile.objects.get(user=user)
            if formset.cleaned_data[0]['DELETE']:
                user.delete()
                profile.delete()
            else:
                profile.birthday = formset.cleaned_data[0]['birthday']
                profile.save()

        else:
            messages.add_message(request, messages.ERROR, formset.errors[0]['user'])

        return HttpResponseRedirect('/account/profile/')


class LoginView(View):
    """ Форма авторизации пользователя """
    pass


class LogoutView(View):
    """ Логаут """
    next_page = None
    pass


class RegistrationView(View):
    """ Форма регистрации нового пользоваетля - клиента"""
    pass


class CartView(View):
    """ Представление для корзины с товарами """
    pass
