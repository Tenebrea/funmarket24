from django import template

from products.utils import format_price

register = template.Library()


@register.filter
def rub(value):
    return format_price(value)
