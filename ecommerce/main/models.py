from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

User = get_user_model()


def is_adult(value):
    adult_age = value + relativedelta(years=18)
    if adult_age > datetime.now().date():  # if adult age is in future
        raise ValidationError('Возраст должен быть не менее 18 лет')


class Vendor(models.Model):

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

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ('name',)

    def __str__(self):
        return self.name


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
        return f"{self.parent_name} > {self.name}"


class Tag(models.Model):

    string = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.string


class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', null=False, default=1, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='Тэг', blank=True)
    vendor = models.ForeignKey(Vendor, verbose_name='Продавец', null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=50, verbose_name='Цвет', blank=True)
    image = models.ImageField(verbose_name='Изображение')
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

    def image_tag(self):
        return mark_safe('<img src="/media/%s" height="50" />' % self.image)

    image_tag.short_description = 'Изображение'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('category', 'title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={'slug': self.slug})


class Delivery(models.Model):
    """ Условия доставки разных типов и условия бесплатной доставки """

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

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    birthday = models.DateField(verbose_name='Дата рождения', validators=[is_adult])

    def __str__(self):
        return self.user.username

