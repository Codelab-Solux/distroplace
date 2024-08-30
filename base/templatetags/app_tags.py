from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from accounts.models import *
from store.models import *
register = template.Library()


# in template arithmetic----------------------------------------
@register.filter
def add(a, b):
    try:
        return int(a) + int(b)
    except (ValueError, TypeError):
        return ''


@register.filter
def subtract(a, b):
    try:
        return int(a) - int(b)
    except (ValueError, TypeError):
        return ''


@register.filter
def multiply(a, b):
    try:
        return int(a) * int(b)
    except (ValueError, TypeError):
        return ''


@register.filter
def divide(a, b):
    try:
        return int(a) / int(b)
    except (ValueError, TypeError):
        return ''

# accounts tags----------------------------------------
@register.filter
def user_orders(pk):
    user = CustomUser.objects.filter(id=pk).first()
    orders = Order.objects.filter(client=user).count()
    return orders

@register.filter
def user_deliveries(pk):
    user = CustomUser.objects.filter(id=pk).first()
    deliveries = Delivery.objects.filter(client=user).count()
    return deliveries


# email splitter ----------------------------------------
@register.filter
def split_email(value):
    return value.split('@')[0]
