from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from store.forms import ProductForm
from store.models import *


def dashboard(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    context = {
        "dashboard": "dash_active",
        'title': 'dashboard',
        'products':products,
        'categories':categories,
        'subcategories':subcategories,
    }
    return render(req, 'dashboard/index.html', context)

# --------------------------------- Products ---------------------------------

def dash_products(req):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        "dash_products": "dash_active",
        'title': 'Products',
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/products.html', context)


def dash_product(req, pk):
    curr_obj = Product.objects.get(id=pk)
    context = {
        "products_page": "dash_active",
        'title': 'Products',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/product.html', context)


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
        "dash_orders": "dash_active",
        'title': 'Orders',
    }
    return render(req, 'dashboard/orders.html', context)


def dash_order(req, pk):
    curr_order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=curr_order)
    rel_orders = Order.objects.filter(
        client=curr_order.client).order_by('-timestamp').exclude(id=pk)[:4]
    context = {
        "order_details": "dash_active",
        'title': 'Order Details',
        'curr_order': curr_order,
        'order_items': order_items,
        'rel_orders': rel_orders,
    }
    return render(req, 'dashboard/order.html', context)


def manage_order(req, pk, kp):
    user = req.user
    curr_order = Order.objects.get(id=pk)

    if kp == 'cancel':
        curr_order.status = 'cancelled'
        curr_order.save()
    elif kp == 'process':
        curr_order.status = 'processed'
        curr_order.save()
        new_delivery = Delivery(
            order=curr_order,
            client=curr_order.client,
            items=curr_order.items,
            phone=curr_order.phone,
            amount_due=curr_order.amount,
        )
        new_delivery.save()

    elif kp == 'deliver':
        curr_order.status = 'delivered'
        curr_order.save()
    else:
        return "error"

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


# --------------------------------- Delivries ---------------------------------

def dash_deliveries(req):
    context = {
        "dash_deliveries": "dash_active",
        'title': 'Deliveries',
    }
    return render(req, 'dashboard/deliveries.html', context)


def dash_delivery(req, pk):
    curr_obj = Delivery.objects.get(id=pk)
    curr_order = Order.objects.get(id=curr_obj.order.id)
    order_items = OrderItem.objects.filter(order=curr_order)
    context = {
        "delivery_details": "dash_active",
        'title': 'Delivery Details',
        'curr_obj': curr_obj,
        'curr_order': curr_order,
        'order_items': order_items,
    }
    return render(req, 'dashboard/delivery.html', context)


def manage_delivery(req, pk, kp):
    pass

# --------------------------Deliveries--------------------------
def promos(req):
    context = {
        "promos": "dash_active",
        'title': 'Promos',
    }
    return render(req, 'dashboard/promos.html', context)

# --------------------------users--------------------------
def clients(req):
    clients = CustomUser.objects.filter(role__id =1)
    context = {
        "customers": "dash_active",
        'title': 'Customers',
        'clients': clients,
    }
    return render(req, 'dashboard/clients.html', context)


def staff_grid(req):
    staff = CustomUser.objects.filter(role__id__gt=1)
    context = {
        "staff": "dash_active",
        'title': 'Staff',
        "staff": staff,
    }
    return render(req, 'dashboard/partials/staff_grid.html', context)

def staff(req):
    staff = CustomUser.objects.filter(role__id__gt=1)
    context = {
        "staff": "dash_active",
        'title': 'Staff',
    }
    return render(req, 'dashboard/staff.html', context)

def finances(req):
    context = {
        "finances": "dash_active",
        'title': 'Finances',
    }
    return render(req, 'dashboard/finances.html', context)

def reports(req):
    context = {
        "reports": "dash_active",
        'title': 'Reports',
    }
    return render(req, 'dashboard/reports.html', context)
