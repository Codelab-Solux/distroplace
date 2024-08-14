from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products/', dash_products, name='dash_products'),
    path('products/add/', add_product, name='add_product'),
    path('products/new/', new_arrivals, name='new_arrivals'),
    path('products/list/', products_list, name='products_list'),
    path('products/grid/', products_grid, name='products_grid'),
    path('products/filter/', filter_products, name='filter_products'),
    path('products/image/add/<hashid:pk>/',
         add_product_image, name='add_product_image'),
    path('products/image/list/<hashid:pk>/',
         product_images, name='product_images'),
    path('products/<hashid:pk>/', dash_product, name='dash_product'),
    path('products/<hashid:pk>/overview/', product_overview, name='product_overview'),
    path('products/<hashid:pk>/edit/', edit_product, name='edit_product'),
    # ----------------------------------------------------------------------------
    path('orders/', dash_orders, name='dash_orders'),
    path('orders/list/', orders_list, name='orders_list'),
    path('orders/filter/', filter_orders, name='filter_orders'),
    path('orders/<hashid:pk>/', dash_order, name='dash_order'),
    path('orders/<hashid:pk>/info/', order_info, name='order_info'),
    path('orders/<hashid:pk>/<str:kp>/manage/',
         manage_order, name='manage_order'),
    # ----------------------------------------------------------------------------
    path('deliveries/', dash_deliveries, name='dash_deliveries'),
    path('deliveries/list/', deliveries_list, name='deliveries_list'),
    path('deliveries/filter/', filter_deliveries, name='filter_deliveries'),
    path('deliveries/<hashid:pk>/', dash_delivery, name='dash_delivery'),
    path('deliveries/<hashid:pk>/info', delivery_info, name='delivery_info'),
    path('deliveries/<hashid:pk>/<str:kp>/manage/',
         manage_delivery, name='manage_delivery'),
    path('promos/', promos, name='promos'),
    path('promos/create/', create_promotion, name='create_promotion'),
    path('promos/list/', promo_list, name='promo_list'),
    path('promos/<hashid:pk>/edit/', edit_promotion, name='edit_promotion'),
    # ----------------------------------------------------------------------------
    path('profile/<hashid:pk>/', dash_profile, name='dash_profile'),
    # ----------------------------------------------------------------------------
    path('clients/', clients, name='clients'),
    path('clients/list/', clients_list, name='clients_list'),
    # ----------------------------------------------------------------------------
    path('staff/', staff, name='staff'),
    path('staff/grid/', staff_grid, name='staff_grid'),
    path('staff/list/', staff_list, name='staff_list'),
    path('staff/<hashid:pk>/', staff_details, name='staff_details'),
    # ----------------------------------------------------------------------------
    path('suppliers/', suppliers, name='suppliers'),
    path('suppliers/create/', create_supplier, name='create_supplier'),
    path('suppliers/list/', suppliers_list, name='suppliers_list'),
    path('suppliers/<hashid:pk>/', supplier_details, name='supplier_details'),
    path('suppliers/<hashid:pk>/edit/', edit_supplier, name='edit_supplier'),
    # ----------------------------------------------------------------------------
    path('finances/', finances, name='finances'),
    path('reports/', reports, name='reports'),
    # ----------------------------------------------------------------------------
    path('parameters/', dash_parameters, name='dash_parameters'),
    path('categories/list/', categories_list, name='categories_list'),
    path('categories/add/', create_category, name='create_category'),
    path('categories/<hashid:pk>/edit/', edit_category, name='edit_category'),
    # --------------------------
    path('subcategories/load/', load_subcategories, name='load_subcategories'),
    path('subcategories/list/', subcategories_list, name='subcategories_list'),
    path('subcategories/add/', create_subcategory, name='create_subcategory'),
    path('subcategories/<hashid:pk>/edit/',
         edit_subcategory, name='edit_subcategory'),
    # --------------------------
    path('delivery_types/list/', delivery_types_list, name='delivery_types_list'),
    path('delivery_types/add/', create_delivery_type,
         name='create_delivery_type'),
    path('delivery_types/<hashid:pk>/edit/',
         edit_delivery_type, name='edit_delivery_type'),
    # --------------------------
    path('promotions/list/', promo_list, name='promo_list'),
    path('promotions/<hashid:pk>/',dash_promo, name='dash_promo'),
    # --------------------------
    path('store/objects/<hashid:pk>/<str:model_name>/delete/',
         delete_store_object, name='delete_store_object'),
]
