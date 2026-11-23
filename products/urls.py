from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('<slug:slug>/', views.catalog, name='catalog'),
    path('<slug:slug>/<int:id>/', views.product, name='product'),
    path('cart/', views.cart, name='cart')
]
