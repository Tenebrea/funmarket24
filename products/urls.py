from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('<slug:slug>/', views.catalog, name='catalog'),
    path('<slug:slug>/<int:id>/', views.product, name='product'),
]
