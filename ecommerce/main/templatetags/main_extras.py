import datetime
from django import template
from ..models import Category, Article

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter(name='reverse_string')
def cut(value):
    return value[-1::-1]


@register.simple_tag
def category_list():
    return Category.objects.all()


@register.simple_tag
def current_category(slug):
    return Category.objects.get(slug=slug)


@register.simple_tag
def article_list():
    return Article.objects.all()
