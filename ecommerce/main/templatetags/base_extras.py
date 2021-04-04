from django import template
from ..models import Parameter

register = template.Library()


@register.simple_tag
def parameter(name):
    return Parameter.objects.get(name=name).value
