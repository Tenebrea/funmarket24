from django import template

from products.utils import format_price

register = template.Library()


@register.filter
def rub(value):
    return format_price(value)

@register.filter
def get_cart_item(mapping, key):
    return mapping.get(key, 0)
