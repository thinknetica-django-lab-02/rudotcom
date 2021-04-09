import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import mark_safe
from django.contrib.auth.models import User, Group
from django.conf import settings
from PIL import Image

from .utils import path_and_rename, upload_avatar
from ecommerce.settings import DEFAULT_GROUP_NAME


class Vendor(models.Model):
    """
    Продавец - одна из ролей класса User
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=64, unique=True, verbose_name='Наименование')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', blank=True)
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, upload_to=upload_avatar)

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        super().save(*args, **kwargs)

        img.thumbnail((200, 200))
        img.save(os.path.join(settings.MEDIA_ROOT, image.name))


class Category(MPTTModel):

    name = models.CharField(max_length=64, unique=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)

    @property
    def parent_name(self):
        return self.parent.name if self.parent else ''

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):

    string = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.string


class Item(models.Model):

    PRODUCT_BIG = (1100, 3000)
    PRODUCT_CARD = (300, 400)
    PRODUCT_THUMB = (50, 50)

    category = models.ForeignKey(Category, verbose_name='Категория', null=False, default=1, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='Тэг', blank=True)
    vendor = models.ForeignKey(Vendor, verbose_name='Продавец', null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=50, verbose_name='Цвет', blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to=path_and_rename)
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    price_discount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена со скидкой',
                                         null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Наличие', default=0)
    display = models.BooleanField(verbose_name='Выставлять', default=True,
                                  blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    visits = models.IntegerField(default=0, verbose_name='👁', help_text='Количество просмотров')
    last_visit = models.DateTimeField(blank=True, null=True, verbose_name='Просмотрен')

    def image_thumb(self):
        return mark_safe('<img src="/media/thumb/%s" height="50" />' % self.image)

    image_thumb.short_description = 'Изображение'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('category', 'title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        ext = image.name.split('.')[-1]
        filename = f'{self.category.slug}_{self.slug}.{ext}'

        img.thumbnail(self.PRODUCT_BIG, Image.ANTIALIAS)
        img.save(os.path.join(settings.MEDIA_ROOT, filename), 'JPEG', quality=95)

        img.thumbnail(self.PRODUCT_CARD, Image.ANTIALIAS)
        img.save(os.path.join(settings.MEDIA_ROOT, 'card', filename), 'JPEG', quality=85)

        img.thumbnail(self.PRODUCT_THUMB)
        img.save(os.path.join(settings.MEDIA_ROOT, 'thumb', filename))

        super().save(*args, **kwargs)


class Delivery(models.Model):
    """
    Условия доставки разных типов и условия бесплатной доставки
    """

    title = models.CharField(max_length=255, verbose_name='Тип доставки')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Стоимость')
    free = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Бесплатно при сумме')
    description = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Условия доставки'

    def __str__(self):
        return f'{self.title} {self.price}р до {self.free}'


class Article(models.Model):
    """
    Простые страницы типа "Контакты" или "Доставка"
    """

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ('id',)

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    name = models.CharField(max_length=50, verbose_name='Пункт меню', null=False, blank=True)
    slug = models.SlugField(unique=True, null=False)
    content = models.TextField(verbose_name='Текст страницы', null=True)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Customer(models.Model):
    """
    Модель Покупатель. При автризации через соцсети создается экземпляр этого класса
    """

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.username


class Parameter(models.Model):

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ('name',)

    name = models.CharField(max_length=255, verbose_name='Имя')
    value = models.CharField(max_length=50, verbose_name='Значение', blank=True)
    meaning = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):

    user = models.ManyToManyField(Customer)

