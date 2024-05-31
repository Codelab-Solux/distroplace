from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products/', dash_products, name='dash_products'),
    path('products/add/', add_product, name='add_product'),
    path('orders/', dash_orders, name='dash_orders'),
    path('deliveries/', deliveries, name='deliveries'),
    path('promos/', promos, name='promos'),
    path('clients/', clients, name='clients'),
    path('staff/', staff, name='staff'),
    path('finances/', finances, name='finances'),
    path('reports/', reports, name='reports'),
]
