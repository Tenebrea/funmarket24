from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('product/', views.product, name='product')
]
