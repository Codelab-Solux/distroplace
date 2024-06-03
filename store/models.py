from django.db import models
from django.urls import reverse
from datetime import date, timedelta
from accounts.models import CustomUser
from utils import *

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='store/categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='store/subcategories/', blank=True, null=True)

    def __str__(self):
        return self.name


unit_types = (
    ('Kg', "Kilos"),
    ('L', "Litres"),
    ('Ut', "Unités"),
)


class Product(models.Model):
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256, default='Générique')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, choices=unit_types)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    price = models.IntegerField(default='0', blank=True, null=True)
    promo_price = models.IntegerField(default='0', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_expirable = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    production_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='product_likes', blank=True)
    is_favorite = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='store/products/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.quantity} - {self.unit}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})


class ShippingInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} - Shipping Info'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('delivery_info', kwargs={'pk': self.pk})


order_statuses = (
    ('pending', "En attente"),
    ('processed', "Traitée"),
    ('delivered', "Livrée"),
    ('cancelled', "Annulée"),
)


class Order(models.Model):
    client = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50, choices=order_statuses, default='pending')
    items = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_hashid(self):
        return h_encode(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.id)

    def get_hashid(self):
        return h_encode(self.id)


delivery_statuses = (
    ('pending', "En attente"),
    ('dispatched', "Expédiée"),
    ('finished', "Terminée"),
    ('cancelled', "Annulée"),
)


class DeliveryType(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=1000)

    def __str__(self):
        return str(self.id)

    def get_hashid(self):
        return h_encode(self.id)


class Delivery(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    items = models.IntegerField(default=0)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    amount_due = models.IntegerField(default=0, blank=True, null=True)
    amount_paid = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=delivery_statuses, default='pending')
    is_vip = models.BooleanField(default=False)
    d_day = models.DateField(default=get_tomorrow)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    observation = models.CharField(max_length=500, blank=True, null=True)
    signature = models.ImageField(
        upload_to='signatures/deliveries/', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_hashid(self):
        return h_encode(self.id)
