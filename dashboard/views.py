from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from store.forms import ProductForm
from store.models import *


def dashboard(req):
    context = {
        "dashboard": "active",
        'title': 'Stores',
    }
    return render(req, 'dashboard/index.html', context)

# --------------------------------- Products ---------------------------------

def dash_products(req):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        "dash_products": "active",
        'title': 'Products',
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/products.html', context)

def add_product(req):
    user= req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    form = ProductForm()
    if req.method == 'POST':
        form = ProductForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau produit ajouté'
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    else:
        return render(req, 'dashboard/partials/prod_form.html', context={'form': form, 'form_title': 'Nouveau Produit'})

# --------------------------------- Products ---------------------------------

def dash_orders(req):
    context = {
        "dash_orders": "active",
        'title': 'Orders',
    }
    return render(req, 'dashboard/orders.html', context)


# --------------------------------- Delivries ---------------------------------

def deliveries(req):
    context = {
        "deliveries": "active",
        'title': 'Deliveries',
    }
    return render(req, 'dashboard/deliveries.html', context)

def promos(req):
    context = {
        "promos": "active",
        'title': 'Promos',
    }
    return render(req, 'dashboard/promos.html', context)

def clients(req):
    clients = CustomUser.objects.filter(role__id =1)
    context = {
        "customers": "active",
        'title': 'Customers',
        'clients': clients,
    }
    return render(req, 'dashboard/clients.html', context)

def staff(req):
    context = {
        "staff": "active",
        'title': 'Staff',
    }
    return render(req, 'dashboard/staff.html', context)

def finances(req):
    context = {
        "finances": "active",
        'title': 'Finances',
    }
    return render(req, 'dashboard/finances.html', context)

def reports(req):
    context = {
        "reports": "active",
        'title': 'Reports',
    }
    return render(req, 'dashboard/reports.html', context)
