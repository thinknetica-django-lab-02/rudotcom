import datetime
from django import template
from ..models import Category

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter(name='reverse_string')
def cut(value):
    return value[-1::-1]


@register.simple_tag
def categories():
    return Category.objects.all()
