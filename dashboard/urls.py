from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products/', dash_products, name='dash_products'),
    path('products/add/', add_product, name='add_product'),
    path('products/<hashid:pk>/', dash_product, name='dash_product'),
    path('orders/', dash_orders, name='dash_orders'),
    path('orders/<hashid:pk>/', dash_order, name='dash_order'),
    path('orders/<hashid:pk>/<str:kp>/manage/', manage_order, name='manage_order'),
    path('deliveries/', dash_deliveries, name='dash_deliveries'),
    path('deliveries/<hashid:pk>/', dash_delivery, name='dash_delivery'),
    path('deliveries/<hashid:pk>/<str:kp>/manage/',
         manage_delivery, name='manage_delivery'),
    path('promos/', promos, name='promos'),
    path('clients/', clients, name='clients'),
    path('staff/', staff, name='staff'),
    path('staff/grid/', staff_grid, name='staff_grid'),
    path('finances/', finances, name='finances'),
    path('reports/', reports, name='reports'),
]
