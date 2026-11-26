from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chip(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    artikul = models.CharField(max_length=6)
    brand = models.CharField(max_length=100)
    in_stock = models.IntegerField()
    manufacturer = models.CharField(max_length=75)
    price = models.IntegerField()
    price_in_bulk = models.IntegerField()
    size = models.CharField(max_length=75)
    color = models.CharField(max_length=75)
    material = models.CharField(max_length=75)
    theme = models.CharField(max_length=100)
    form = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=None)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='products')
    chip = models.ForeignKey(Chip, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    thumbnail_img = models.ImageField(upload_to='products/thumbnails/', default=None, null=True, blank=True)
    
    def __str__(self):
        return self.title


class Subcategory(models.Model):
    name = models.CharField()
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, unique=True)
    
class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    is_bulk = models.BooleanField(default=False)
    
class OrderStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=200)
    flat = models.CharField(max_length=20, null=True)
    entrance = models.CharField(max_length=20, null=True)
    floor = models.IntegerField(null=True)
    phone = models.CharField(max_length=13)
    name = models.CharField(max_length=50)
    comment = models.TextField(null=True)
    email = models.EmailField()
    delivery_price = models.IntegerField()
    price = models.IntegerField()
    status = models.ForeignKey(OrderStatus, related_name='status', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Заказ №{self.id}"
    