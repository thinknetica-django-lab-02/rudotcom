from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget

from .models import Category, Tag, Vendor, Item, Article, Customer


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent', 'slug']
    list_display = ('name', 'parent', 'slug')
    ordering = ['parent', 'name', ]
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
                     ('image', 'image_tag',), 'description', 'tag', 'display', 'color',
                     ]
          }
         ),
        ('Служебная информация',
         {'fields': ['slug', 'date_added', 'visits', 'last_visit', ],
          'classes': ['collapse']
          }
         ),
    ]
    readonly_fields = ['image_tag', 'visits', 'last_visit', 'date_added', ]
    list_display = ('title', 'image_tag', 'visits', 'category', 'price', 'price_discount', 'quantity', 'display')
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


admin.site.site_header = "Маркетплейс. Панель управления"
admin.site.unregister(Group)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Tag)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Article, ArticleAdmin)
