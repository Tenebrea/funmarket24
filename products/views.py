from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

SORT_OPTIONS = {
    'price': 'price',
    '-price': '-price',
    'title': 'title',
    '-title': '-title',
    'stock': '-in_stock',
}

MULTI_FILTERS = ('size', 'color', 'material', 'theme', 'form')


# Create your views here.
def catalog(request, slug):
    category = get_object_or_404(Category, slug=slug)
    base = Product.objects.filter(category=category)
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

    sort = request.GET.get('sort', 'price')
    products = products.order_by(SORT_OPTIONS.get(sort, 'price'))

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
        'categories': Category.objects.all(),
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
    product = get_object_or_404(Product, id=id, category=category)
    
    return render(request, 'catalog/product.html', {'product': product, 'category': category, 'categories': Category.objects.all()})
