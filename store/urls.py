from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', store, name='store'),
    # ----------------------- products ------------------------------
    path('products/', products, name='products'),
    path('products/<hashid:pk>/', product_details, name='product_details'),
    # ----------------------- cart ------------------------------
    path('cart/', cart, name='cart'),
    path('cart/add_item/', add_to_cart, name='add_to_cart'),
    path('cart/remove_item/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear_item/', clear_from_cart, name='clear_cart'),
    path('cart/clear/', clear_cart, name='cart_remove'),
    path('cart/resume/', cart_resume, name='cart_resume'),
    path('checkout/', checkout, name='checkout'),
    # ----------------------- orders ------------------------------
    path('orders/', orders, name='orders'),
    path('orders/new/', place_order, name='place_order'),
    path('orders/resume/', orders_resume, name='orders_resume'),
    path('orders/<hashid:pk>/', order_details, name='order_details'),
    path('orders/<hashid:pk>/cancel/', cancel_order, name='cancel_order'),
    # ----------------------- deliveries ------------------------------
    path('deliveries/', deliveries, name='deliveries'),
    path('deliveries/resume/', deliveries_resume, name='deliveries_resume'),
    path('deliveries/new/<hashid:pk>/', new_delivery, name='new_delivery'),
    path('deliveries/<hashid:pk>/', delivery_details, name='delivery_details'),
    path('deliveries/<hashid:pk>/postpone/',
         postpone_delivery, name='postpone_delivery'),
]
