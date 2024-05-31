from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', store, name='store'),
    # ----------------------- products ------------------------------
    path('products/', products, name='products'),
    path('products/list/', products_list, name='products_list'),
    path('products/grid/', products_grid, name='products_grid'),
    path('products/filter/', filter_products, name='filter_products'),
    path('products/<hashid:pk>/', product_details, name='product_details'),
    # ----------------------- cart ------------------------------
    path('cart/', cart, name='cart'),
    path('cart/add_item/', add_to_cart, name='add_to_cart'),
    path('cart/remove_item/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear_item/', clear_from_cart, name='clear_cart'),
    path('cart/clear/', clear_cart, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
    # ----------------------- orders ------------------------------
    path('orders/', orders, name='orders'),
    path('orders/list/', orders_list, name='orders_list'),
    path('orders/filter/', filter_orders, name='filter_orders'),
    path('orders/new/', place_order, name='place_order'),
]
