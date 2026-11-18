from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def catalog(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.select_related('chip').filter(category=category).order_by('price')
    
    return render(request, 'catalog/catalog.html', {'products': products, 'category': category, 'categories': Category.objects.all()})

def product(request, id, slug):
    category = get_object_or_404(Category, slug=slug)
    product = get_object_or_404(Product, id=id, category=category)
    
    return render(request, 'catalog/product.html', {'product': product, 'category': category, 'categories': Category.objects.all()})