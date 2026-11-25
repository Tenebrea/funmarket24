from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Subcategory, Cart, CartProduct, Order, OrderStatus
from django.views.decorators.http import require_POST


SORT_OPTIONS = {
    'price': 'price',
    '-price': '-price',
    'title': 'title',
    '-title': '-title',
    'stock': '-in_stock',
}

MULTI_FILTERS = ('size', 'color', 'material', 'theme', 'form')

DEFAULT_SORT = '-price'


# Create your views here.
def catalog(request, slug):
    category = get_object_or_404(Category, slug=slug)

    subcategory_slug = request.GET.get('subcategory')
    subcategory = None

    base = Product.objects.filter(category=category)
    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
        base = base.filter(subcategory=subcategory)

    products = base.select_related('chip')

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    manufacturer = request.GET.get('manufacturer')
    if manufacturer:
        products = products.filter(manufacturer=manufacturer)

    for field in MULTI_FILTERS:
        values = request.GET.getlist(field)
        if values:
            products = products.filter(**{f'{field}__in': values})

    sort = request.GET.get('sort', DEFAULT_SORT)
    products = products.order_by(SORT_OPTIONS.get(sort, DEFAULT_SORT))

    bounds = base.aggregate(lo=Min('price'), hi=Max('price'))
    price_lo = bounds['lo'] if bounds['lo'] is not None else 0
    price_hi = bounds['hi'] if bounds['hi'] is not None else 0

    options = {
        field: base.exclude(**{field: ''})
        .values_list(field, flat=True)
        .distinct()
        .order_by(field)
        for field in ('manufacturer',) + MULTI_FILTERS
    }

    return render(request, 'catalog/catalog.html', {
        'products': products,
        'category': category,
        'subcategory': subcategory,
        'categories': Category.objects.prefetch_related('subcategory_set'),
        'manufacturers': options['manufacturer'],
        'sizes': options['size'],
        'colors': options['color'],
        'materials': options['material'],
        'themes': options['theme'],
        'forms': options['form'],
        'selected': {
            'manufacturer': manufacturer or '',
            **{field: request.GET.getlist(field) for field in MULTI_FILTERS},
        },
        'price_lo': price_lo,
        'price_hi': price_hi,
        'current_sort': sort,
    })


def product(request, id, slug):
    category = get_object_or_404(Category, slug=slug)
    product = get_object_or_404(
        Product.objects.prefetch_related('images'),
        id=id,
        category=category,
    )
    
    return render(request, 'catalog/product.html', {'product': product, 'category': category, 'categories': Category.objects.all()})

def plural(number, forms):
    number = abs(number) % 100
    if 11 <= number <= 14:
        return forms[2]

    number %= 10
    if number == 1:
        return forms[0]
    if 2 <= number <= 4:
        return forms[1]

    return forms[2]

@login_required
@require_POST
def add_to_cart(request):
    product_id = int(request.POST.get('product', ''))
    amount = int(request.POST.get('amount'))
    
    product = get_object_or_404(Product, pk=product_id)
    
    
    if amount == 0: return redirect('products:catalog', slug=product.category.slug)
    
    if (amount>product.in_stock):
        amount = product.in_stock
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if amount == 0:
        CartProduct.objects.filter(cart=cart, product=product).delete()
    else:
        is_bulk = amount > 50
        CartProduct.objects.update_or_create(cart=cart, product=product, defaults={'amount': amount, 'is_bulk': is_bulk})    
    
    return redirect('products:catalog', slug=product.category.slug)

def cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item_id = request.POST.get('item')
        if item_id:
            CartProduct.objects.filter(cart__user=request.user, pk=item_id).delete()
        return redirect('products:cart')

    items = []
    total = 0
    count = 0

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)

        for item in cart.products.select_related('product', 'product__chip', 'product__category'):
            line_total = item.product.price * item.amount
            line_total_bulk = item.product.price_in_bulk * item.amount

            items.append({
                'id': item.id,
                'product': item.product,
                'amount': item.amount,
                'line_total': line_total,
                'line_total_bulk': line_total_bulk,
            })

            total += line_total
            count += item.amount

    return render(request, 'catalog/cart.html', {
        'items': items,
        'item_count': count,
        'item_word': plural(count, ('товар', 'товара', 'товаров')),
        'total': total,
        'categories': Category.objects.prefetch_related('subcategory_set'),
    })
    
@login_required
def order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = list(cart.products.select_related('product'))

    if not items:
        return redirect('products:cart')
    
    delivery = 990
    total = sum(item.product.price * item.amount for item in items) + delivery
    
    order = None
    
    if request.method == 'POST':
        status, _ = OrderStatus.objects.get_or_create(
            id=1, defaults={'name': 'Новый'},
        )
        try:
            floor = int(request.POST.get('floor') or 0)
        except ValueError:
            floor = 0
        order = Order.objects.create(
            id=(Order.objects.aggregate(max_id=Max('id'))['max_id'] or 0) + 1,
            address=request.POST.get('address', ''),
            flat=request.POST.get('flat', ''),
            entrance=request.POST.get('entrance', ''),
            floor=floor,
            phone=request.POST.get('phone', ''),
            name=request.POST.get('name', ''),
            comment=request.POST.get('comment', ''),
            email=request.POST.get('email', ''),
            delivery_price=990,
            price=total,
            status=status,
            user=request.user,
        )

        cart.products.all().delete()

    

    return render(request, 'catalog/order.html', {
        'order': order,
        'categories': Category.objects.prefetch_related('subcategory_set'),
        'total': total,
        'delivery': delivery
    })