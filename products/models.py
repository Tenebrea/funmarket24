from django.db import models
from filer.fields.image import FilerImageField

from core.settings import MEDIA_ROOT

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
    chip = models.ForeignKey(Chip, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    thumbnail_img = models.ImageField(upload_to=MEDIA_ROOT, default=None, null=True)
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = FilerImageField(null=True, related_name="product_images", on_delete=models.CASCADE)