from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def url_with(context, **kwargs):
    """Return the current querystring with the given params replaced.

    A value of None removes the param; the page param is always dropped.
    """
    request = context.get('request')
    params = request.GET.copy() if request else QueryDict(mutable=True)

    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value

    params.pop('page', None)
    encoded = params.urlencode()

    return f'?{encoded}' if encoded else ''
