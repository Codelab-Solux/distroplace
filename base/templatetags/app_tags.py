from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Sum
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
