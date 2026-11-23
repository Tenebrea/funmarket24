from django.db.models import ExpressionWrapper, F, IntegerField, Sum

from .models import CartProduct
from .utils import format_price


def cart_summary(request):
    if not request.user.is_authenticated:
        return {'cart_item_count': 0, 'cart_total_display': format_price(0)}

    totals = CartProduct.objects.filter(cart__user=request.user).aggregate(
        count=Sum('amount'),
        total=Sum(ExpressionWrapper(
            F('product__price') * F('amount'),
            output_field=IntegerField(),
        )),
    )

    return {
        'cart_item_count': totals['count'] or 0,
        'cart_total_display': format_price(totals['total'] or 0),
    }
