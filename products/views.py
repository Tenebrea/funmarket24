from django.shortcuts import render
from .models import Product

# Create your views here.
def catalog(request):
    products = Product.objects.select_related('chip').order_by('price')
    return render(request, 'catalog/catalog.html', {'products': products})

def product(request):
    return render(request, 'catalog/product.html')