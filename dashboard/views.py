from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.contrib import messages
from base.models import Promotion
from store.forms import *
from store.models import *


def dashboard(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    promotions = Promotion.objects.filter(is_active=True)

    context = {
        "dashboard": "dash_active",
        'title': 'dashboard',
        'products':products,
        'promotions':promotions,
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


def new_arrivals(req):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.filter(is_new=True)
    objects = paginate_objects(req, products)
    context = {
        "dash_products": "dash_active",
        'title': 'Products',
        'objects': objects,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/new_arrivals.html', context)


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
        return render(req, 'dashboard/partials/product_form.html', context={'form': form, 'form_title': 'Nouveau Produit'})


@login_required(login_url='login')
def edit_product(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    curr_obj = get_object_or_404(Product, id=pk)

    form = ProductForm(instance=curr_obj)
    if req.method == 'POST':
        form = ProductForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Données modifiée avec success')
        return redirect('dash_product', pk=curr_obj.id)
    else:
        return render(req, 'dashboard/partials/product_form.html', context={'form': form, 'form_title': 'Modifier ce produit', 'curr_obj': curr_obj})

def products_list(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'dashboard/partials/products_list.html', context)


def products_grid(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'dashboard/partials/products_grid.html', context)


def filter_products(req):
    name_query = req.POST.get('name')
    price_query = req.POST.get('price')
    quantity_query = req.POST.get('quantity')
    category_query = req.POST.get('category')
    subcategory_query = req.POST.get('subcategory')
    promo_query = req.POST.get('is_promoted')
    exp_query = req.POST.get('is_expirable')
    prod_date_query = req.POST.get('prod_date')
    exp_date_query = req.POST.get('exp_date')

    base_query = Product.objects.all().order_by('name')

    if name_query:
        base_query = base_query.filter(name=name_query)
    if price_query:
        base_query = base_query.filter(price=price_query)
    if quantity_query:
        base_query = base_query.filter(quantity=quantity_query)
    if category_query:
        base_query = base_query.filter(category__id=category_query)
    if subcategory_query:
        base_query = base_query.filter(subcategory__id=subcategory_query)
    if exp_query:
        base_query = base_query.filter(is_expirable=exp_query)
    if promo_query:
        base_query = base_query.filter(is_promoted=promo_query)

    products = base_query

    context = {"products": products}

    return render(req, 'dashboard/partials/products_list.html', context)

# --------------------------------- Products ---------------------------------
def dash_orders(req):
    context = {
        "dash_orders": "dash_active",
        'title': 'Orders',
    }
    return render(req, 'dashboard/orders.html', context)



def dash_order(req, pk):
    curr_obj = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=curr_obj)
    rel_orders = Order.objects.filter(
        client=curr_obj.client).order_by('-timestamp').exclude(id=pk)[:4]
    context = {
        "order_details": "dash_active",
        'title': 'Order Details',
        'curr_obj': curr_obj,
        'order_items': order_items,
        'rel_orders': rel_orders,
    }
    return render(req, 'dashboard/order.html', context)


def manage_order(req, pk, kp):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    
    curr_obj = Order.objects.get(id=pk)

    if kp == 'cancel':
        curr_obj.status = 'cancelled'
        curr_obj.save()
    elif kp == 'process':
        curr_obj.status = 'processed'
        curr_obj.save()

    elif kp == 'deliver':
        curr_obj.status = 'delivered'
        curr_obj.save()
    else:
        HttpResponse("error", status=400)

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


def orders_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    orders = Order.objects.all().order_by('-timestamp')
    context = {
        'orders': orders,
    }
    return render(req, 'dashboard/partials/orders_list.html', context)


def filter_orders(req):
    user = req.user
    # user_query = req.POST.get('user')
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    phone_query = req.POST.get('phone')
    amount_query = req.POST.get('amount')
    items_query = req.POST.get('items')
    status_query = req.POST.get('status')

    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    else:
        base_query = Order.objects.all().order_by('-timestamp')

    # if user_query:
    #     base_query = base_query.filter(user_)

    if min_date_query:
        base_query = base_query.filter(timestamp__date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(timestamp__date__lte=max_date_query)
    if phone_query:
        base_query = base_query.filter(phone=phone_query)
    if amount_query:
        base_query = base_query.filter(amount=amount_query)
    if items_query:
        base_query = base_query.filter(items=items_query)
    if status_query:
        base_query = base_query.filter(status=status_query)

    orders = base_query

    context = {"orders": orders}

    return render(req, 'dashboard/partials/orders_list.html', context)


def order_info(req, pk):
    curr_obj = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=curr_obj)
    shipping_info = ShippingInfo.objects.filter(user=curr_obj.client).first()
    context = {
        "delivery_details": "dash_active",
        'title': 'Delivery Details',
        'curr_obj': curr_obj,
        'order_items': order_items,
        'shipping_info': shipping_info,
    }
    return render(req, 'dashboard/partials/order_info.html', context)


# --------------------------------- Delivries ---------------------------------
def dash_deliveries(req):
    context = {
        "dash_deliveries": "dash_active",
        'title': 'Deliveries',
    }
    return render(req, 'dashboard/deliveries.html', context)


def deliveries_list(req):
    user = req.user
    deliveries = Delivery.objects.all().order_by('-timestamp')
    context = {
        'deliveries': deliveries,
    }
    return render(req, 'dashboard/partials/deliveries_list.html', context)


def dash_delivery(req, pk):
    curr_obj = Delivery.objects.get(id=pk)
    curr_order = Order.objects.get(id=curr_obj.order.id)
    order_items = OrderItem.objects.filter(order=curr_order)
    shipping_info = ShippingInfo.objects.filter(user=curr_obj.client).first()
    context = {
        "delivery_details": "dash_active",
        'title': 'Delivery Details',
        'curr_obj': curr_obj,
        'curr_order': curr_order,
        'order_items': order_items,
        'shipping_info': shipping_info,
    }
    return render(req, 'dashboard/delivery.html', context)

def delivery_info(req, pk):
    curr_obj = Delivery.objects.get(id=pk)
    curr_order = Order.objects.get(id=curr_obj.order.id)
    order_items = OrderItem.objects.filter(order=curr_order)
    shipping_info = ShippingInfo.objects.filter(user=curr_obj.client).first()
    context = {
        "delivery_details": "dash_active",
        'title': 'Delivery Details',
        'curr_obj': curr_obj,
        'curr_order': curr_order,
        'order_items': order_items,
        'shipping_info': shipping_info,
    }
    return render(req, 'dashboard/partials/delivery_info.html', context)


def manage_delivery(req, pk, kp):
    user = req.user
    curr_obj = Delivery.objects.get(id=pk)

    if kp == 'cancel':
        curr_obj.status = 'cancelled'
        curr_obj.is_cancelled = True
        curr_obj.save()

    elif kp == 'dispatch':
        curr_obj.status = 'dispatched'
        curr_obj.save()

    elif kp == 'finish':
        curr_obj.status = 'finished'
        curr_obj.save()
        
    elif kp == 'postpone':
        new_dday = 'Date'
        curr_obj.dday = new_dday
        curr_obj.save()

    else:
        HttpResponse("error", status=400)

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


def filter_deliveries(req):
    user = req.user
    # user_query = req.POST.get('user')
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    phone_query = req.POST.get('phone')
    amount_query = req.POST.get('amount')
    items_query = req.POST.get('items')
    status_query = req.POST.get('status')

    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    else:
        base_query = Delivery.objects.all().order_by('-timestamp')

    # if user_query:
    #     base_query = base_query.filter(user_)

    if min_date_query:
        base_query = base_query.filter(dday__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(dday__lte=max_date_query)
    if phone_query:
        base_query = base_query.filter(phone=phone_query)
    if amount_query:
        base_query = base_query.filter(amount_due=amount_query)
    if items_query:
        base_query = base_query.filter(items=items_query)
    if status_query:
        base_query = base_query.filter(status=status_query)

    deliveries = base_query

    context = {"deliveries": deliveries}

    return render(req, 'dashboard/partials/deliveries_list.html', context)


# --------------------------Promotions--------------------------
def promos(req):
    context = {
        "promos": "dash_active",
        'title': 'Promos',
    }
    return render(req, 'dashboard/promos.html', context)


def dash_promo(req, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    products = promotion.products.all()
    context = {
        "promo_page": "active",
        'title': 'Promo Details',
        'promotion': promotion,
        'products': products,
    }
    return render(req, 'dashboard/promo_details.html', context)


def promo_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    else:
        promotions = Promotion.objects.all().order_by('-timestamp')
    context = {
        'promotions': promotions,
    }
    return render(req, 'dashboard/partials/promo_list.html', context)

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
    context = {
        "staff": "dash_active",
        'title': 'Staff',
    }
    return render(req, 'dashboard/staff.html', context)

def staff_details(req,pk):
    curr_obj = CustomUser.objects.get(id=pk)
    context = {
        "staff": "dash_active",
        'title': 'Staff',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/staff_details.html', context)


# --------------------------finances--------------------------
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


# --------------------------Parameters--------------------------
def dash_parameters(req):
    context = {
        "dash_parameters": "dash_active",
        'title': 'Parameters',
    }
    return render(req, 'dashboard/parameters.html', context)


def categories_list(req):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(req, 'dashboard/partials/categories_list.html', context)


@login_required(login_url='login')
def create_category(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect('home')

    form = CategoryForm()
    if req.method == 'POST':
        form = CategoryForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Nouvelle catégorie'})


@login_required(login_url='login')
def edit_category(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    curr_obj = get_object_or_404(Category, id=pk)

    form = CategoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = CategoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Données modifiée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Modifier cette catégorie', 'curr_obj': curr_obj})


def subcategories_list(req):
    subcategories = SubCategory.objects.all().order_by('name')
    context = {
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/partials/subcategories_list.html', context)

@login_required(login_url='login')
def create_subcategory(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect('home')

    form = SubCategoryForm()
    if req.method == 'POST':
        form = SubCategoryForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle sous-catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Nouvelle sous-catégorie'})


@login_required(login_url='login')
def edit_subcategory(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    curr_obj = get_object_or_404(SubCategory, id=pk)

    form = SubCategoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = SubCategoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Données modifiée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Modifier cette sous-catégorie', 'curr_obj': curr_obj})
    
def delivery_types_list(req):
    delivery_types = DeliveryType.objects.all()
    context = {
        'delivery_types': delivery_types,
    }
    return render(req, 'dashboard/partials/delivery_types_list.html', context)


@login_required(login_url='login')
def create_delivery_type(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect('home')

    form = DeliveryTypeForm()
    if req.method == 'POST':
        form = DeliveryTypeForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle sous-catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Nouveau type de lvraison'})


@login_required(login_url='login')
def edit_delivery_type(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    curr_obj = get_object_or_404(SubCategory, id=pk)

    form = SubCategoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = SubCategoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Données modifiée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Modifier ce type de lvraison', 'curr_obj': curr_obj})


# secures the delete route and makes it only accessible by the DELETE method
@login_required(login_url='login')
@require_http_methods(['DELETE'])
def delete_store_object(req, pk, model_name):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    
    try:
        # Get the model class from the model name
        ModelClass = apps.get_model('store', model_name)
    except LookupError:
        return HttpResponse(status=404)  # Model not found

    # Fetch the object to be deleted
    obj = get_object_or_404(ModelClass, pk=pk)

    # Check user's permission
    if req.user.role.sec_level < 4:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))

    # Delete the object
    obj.delete()

    # Return a success response
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
