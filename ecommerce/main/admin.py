from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget

from .models import Category, Tag, Vendor, Item, Article, Customer, Parameter


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 40
    fields = ['name', 'parent', 'slug']
    list_display = ('name', 'slug')
    list_filter = ['parent']
    prepopulated_fields = {"slug": ("name",)}


class ItemAdminForm(ModelForm):

    description = forms.CharField(label='Описание', widget=CKEditorWidget())


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    # change_form_template = 'admin.html'
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        ('Товар',
         {'fields': ['title', 'category', 'price', 'price_discount', 'quantity', 'vendor',
                     ('image', 'image_thumb',), 'description', 'tag', 'display', 'color',
                     ]
          }
         ),
        ('Служебная информация',
         {'fields': ['slug', 'date_added', 'visits', 'last_visit', ],
          'classes': ['collapse']
          }
         ),
    ]
    readonly_fields = ['image_thumb', 'visits', 'last_visit', 'date_added', ]
    list_display = ('title', 'image_thumb', 'visits', 'category', 'price', 'price_discount', 'quantity', 'display')
    list_filter = ['display', ]
    search_fields = ['title', 'description']
    ordering = ('-date_added', 'title', 'category', 'price', 'quantity')


class ArticleAdminForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    content = forms.CharField(label='Текст страницы', widget=CKEditorWidget())


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

    fieldsets = (
        (None, {'fields': ('slug', 'name', 'title', 'content',)}),
    )
    list_display = ('name', 'title', 'slug',)


class ParameterAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'value', 'meaning',)}),
    )
    readonly_fields = ['name', ]
    list_display = ('name', 'value',)

    # убрать кнопку "Удалить"
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "Маркетплейс. Панель управления"
admin.site.unregister(Group)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Tag)
admin.site.register(Item, ItemAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CustomMPTTModelAdmin)
admin.site.register(Parameter, ParameterAdmin)
