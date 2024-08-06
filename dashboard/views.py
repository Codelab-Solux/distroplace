from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.contrib import messages
from base.models import Promotion
from store.forms import *
from store.models import *


@login_required(login_url='login')
def dashboard(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    promotions = Promotion.objects.filter(is_active=True)

    context = {
        "dashboard": "dash_active",
        'title': 'dashboard',
        'products': products,
        'promotions': promotions,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/index.html', context)


# ------------------------------------------------- Products -------------------------------------------------
@login_required(login_url='login')
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


@login_required(login_url='login')
def new_arrivals(req):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.filter(is_new=True).order_by('-name')
    objects = paginate_objects(req, products)
    context = {
        "dash_products": "dash_active",
        'title': 'Products',
        'objects': objects,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'dashboard/new_arrivals.html', context)


@login_required(login_url='login')
def dash_product(req, pk):
    curr_obj = Product.objects.get(id=pk)
    context = {
        "dash_products": "dash_active",
        'title': 'Dashboard Products',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/product_details.html', context)


@login_required(login_url='login')
def product_overview(req, pk):
    curr_obj = Product.objects.get(id=pk)
    context = {
        "products_page": "dash_active",
        'title': 'Products',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/partials/product_overview.html', context)


@login_required(login_url='login')
def add_product(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProductForm()
    context = {
        "dash_products": "dash_active",
        'title': 'Products',
        'form': form,
        'form_title': 'Ajouter un produit'
    }
    if req.method == 'POST':
        form = ProductForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            messages.success(req, 'Nouveau produit ajouté')
            return redirect('new_arrivals')
    else:
        return render(req, 'dashboard/product_form.html', context)


@login_required(login_url='login')
def edit_product(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=curr_obj)

    if req.method == 'POST':
        form = ProductForm(req.POST, req.FILES, instance=curr_obj)
        if form.is_valid():
            form.save()
            messages.success(req, 'Données modifiée avec succès')
            return redirect('dash_product', pk=curr_obj.id)

    context = {
        'title': 'Products',
        'form': form,
        'form_title': 'Modifier ce produit',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/product_form.html', context)


@login_required(login_url='login')
def products_list(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'dashboard/partials/products_list.html', context)


@login_required(login_url='login')
def products_grid(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'dashboard/partials/products_grid.html', context)


@login_required(login_url='login')
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


def load_subcategories(req):
    category_id = req.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).all()
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


@login_required(login_url='login')
def add_product_image(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Product, id=pk)

    if req.method == 'POST':
        images = req.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                product=curr_obj,
                image=image
            )
        messages.success(req, 'Images ajoutée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'data_changed'})
    else:
        return render(req, 'dashboard/components/image_form.html')


def product_images(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Product, id=pk)
    prod_images = ProductImage.objects.filter(product=curr_obj)
    is_favorite = False

    if user.is_authenticated:
            is_favorite = curr_obj.likes.filter(id=user.id).exists()

    context = {
        'curr_obj': curr_obj,
        'prod_images': prod_images,
        'is_favorite': is_favorite,
    }

    return render(req, 'dashboard/partials/product_images.html', context)


# ------------------------------------------------- Orders -------------------------------------------------


@login_required(login_url='login')
def dash_orders(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    context = {
        "dash_orders": "dash_active",
        'title': 'Orders',
    }
    return render(req, 'dashboard/orders.html', context)


@login_required(login_url='login')
def dash_order(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

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
    return render(req, 'dashboard/order_details.html', context)


@login_required(login_url='login')
def manage_order(req, pk, kp):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

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


@login_required(login_url='login')
def orders_list(req):
    orders = Order.objects.all().order_by('-timestamp')
    context = {
        'orders': orders,
    }
    return render(req, 'dashboard/partials/orders_list.html', context)


@login_required(login_url='login')
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
        return redirect('home')

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


@login_required(login_url='login')
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


# ------------------------------------------------- Delivries -------------------------------------------------
@login_required(login_url='login')
def dash_deliveries(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "dash_deliveries": "dash_active",
        'title': 'Deliveries',
    }
    return render(req, 'dashboard/deliveries.html', context)


@login_required(login_url='login')
def deliveries_list(req):
    deliveries = Delivery.objects.all().order_by('-timestamp')
    context = {
        'deliveries': deliveries,
    }
    return render(req, 'dashboard/partials/deliveries_list.html', context)


@login_required(login_url='login')
def dash_delivery(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

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


@login_required(login_url='login')
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


@login_required(login_url='login')
def manage_delivery(req, pk, kp):
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


@login_required(login_url='login')
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
        return redirect('home')

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


# -------------------------------------------------Promotions-------------------------------------------------
@login_required(login_url='login')
def promos(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "promos": "dash_active",
        'title': 'Promos',
    }
    return render(req, 'dashboard/promos.html', context)


@login_required(login_url='login')
def dash_promo(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    promotion = get_object_or_404(Promotion, pk=pk)
    products = promotion.products.all()
    context = {
        "promo_page": "active",
        'title': 'Promo Details',
        'promotion': promotion,
        'products': products,
    }
    return render(req, 'dashboard/promo_details.html', context)


@login_required(login_url='login')
def promo_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    else:
        promotions = Promotion.objects.all().order_by('-timestamp')
    context = {
        'promotions': promotions,
    }
    return render(req, 'dashboard/partials/promo_list.html', context)


# ------------------------------------------------- Clients-------------------------------------------------
@login_required(login_url='login')
def clients(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = CustomUser.objects.filter(role__id=1)
    context = {
        "clients_page": "dash_active",
        'title': 'Customers',
        'clients': clients,
    }
    return render(req, 'dashboard/clients.html', context)


@login_required(login_url='login')
def clients_list(req):
    clients = CustomUser.objects.filter(role__id=1)
    context = {
        'clients': clients,
    }
    return render(req, 'accounts/partials/clients_list.html', context)


# ------------------------------------------------- Staff -------------------------------------------------
@login_required(login_url='login')
def staff(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "staff_page": "dash_active",
        'title': 'Staff',
    }
    return render(req, 'dashboard/staff.html', context)


@login_required(login_url='login')
def staff_list(req):
    staff = CustomUser.objects.filter(role__id__gt=1, is_staff=True)
    context = {
        'staff': staff,
    }
    return render(req, 'accounts/partials/staff_list.html', context)


@login_required(login_url='login')
def staff_grid(req):
    staff = CustomUser.objects.filter(role__id__gt=1, is_staff=True)
    context = {
        'title': 'Staff',
        "staff": staff,
    }
    return render(req, 'dashboard/partials/staff_grid.html', context)


@login_required(login_url='login')
def staff_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = CustomUser.objects.get(id=pk)
    context = {
        "staff": "dash_active",
        'title': 'Staff',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/staff_details.html', context)

# ------------------------------------------------- Suppliers -------------------------------------------------


@login_required(login_url='login')
def suppliers(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "suppliers_page": "dash_active",
        'title': 'Fournisseurs',
    }
    return render(req, 'dashboard/suppliers.html', context)


@login_required(login_url='login')
def supplier_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = Supplier.objects.get(id=pk)
    available_products = Product.objects.filter(
        supplier=curr_obj).order_by('-name')
    received_products = Product.objects.filter(
        supplier=curr_obj).order_by('-name')
    returned_products = Product.objects.filter(
        supplier=curr_obj).order_by('-name')
    context = {
        "suppliers": "dash_active",
        'title': 'Fournisseur',
        'curr_obj': curr_obj,
        'available_products': available_products,

        'received_products': received_products,
        'returned_products': returned_products,
    }
    return render(req, 'dashboard/supplier_details.html', context)


@login_required(login_url='login')
def suppliers_list(req):
    suppliers = Supplier.objects.all().order_by('name')
    context = {
        'suppliers': suppliers,
    }
    return render(req, 'dashboard/partials/suppliers_list.html', context)


@login_required(login_url='login')
def create_supplier(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = SupplierForm()
    if req.method == 'POST':
        form = SupplierForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Nouveau fournisseur'})


@login_required(login_url='login')
def edit_supplier(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Supplier, id=pk)

    form = SupplierForm(instance=curr_obj)
    if req.method == 'POST':
        form = SupplierForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
            # messages.success(req, 'Données modifiée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Modifier ce fournisseur', 'curr_obj': curr_obj})

# ------------------------------------------------- Finances -------------------------------------------------


@login_required(login_url='login')
def finances(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "finances": "dash_active",
        'title': 'Finances',
    }
    return render(req, 'dashboard/finances.html', context)


@login_required(login_url='login')
def reports(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "reports": "dash_active",
        'title': 'Reports',
    }
    return render(req, 'dashboard/reports.html', context)


# ------------------------------------------------- Parameters -------------------------------------------------
@login_required(login_url='login')
def dash_parameters(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "dash_parameters": "dash_active",
        'title': 'Parameters',
    }
    return render(req, 'dashboard/parameters.html', context)


@login_required(login_url='login')
def categories_list(req):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(req, 'dashboard/partials/categories_list.html', context)


@login_required(login_url='login')
def create_category(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
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
        return redirect('home')

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


@login_required(login_url='login')
def subcategories_list(req):
    subcategories = SubCategory.objects.all().order_by('name')
    context = {
        'subcategories': subcategories,
        'title': 'titleeeeeeeeeee',
    }
    return render(req, 'dashboard/partials/subcategories_list.html', context)


@login_required(login_url='login')
def create_subcategory(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
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
        return redirect('home')

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


@login_required(login_url='login')
def delivery_types_list(req):
    delivery_types = DeliveryType.objects.all()
    context = {
        'delivery_types': delivery_types,
    }
    return render(req, 'dashboard/partials/delivery_types_list.html', context)


@login_required(login_url='login')
def create_delivery_type(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
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
        return redirect('home')

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

@require_http_methods(['DELETE'])
@login_required(login_url='login')
def delete_store_object(req, pk, model_name):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

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


@login_required(login_url='login')
def dash_profile(req, pk):
    curr_obj = CustomUser.objects.get(id=pk)
    context = {
        'title': 'Profil',
        'curr_obj': curr_obj,
    }
    return render(req, 'dashboard/profile.html', context)
