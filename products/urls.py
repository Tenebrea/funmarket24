from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('<slug:slug>/', views.catalog, name='catalog'),
    path('<slug:slug>/<int:id>/', views.product, name='product'),
]
