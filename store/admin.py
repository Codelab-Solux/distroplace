from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductComment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingInfo)
admin.site.register(DeliveryType)
admin.site.register(Delivery)
