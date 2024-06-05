from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import Q
from store.forms import *
from .models import *
from .cart import Cart


def store(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    orders = Order.objects.all()
    deliveries = Delivery.objects.all()
    context = {
        "store_page": "active",
        'title': 'Store',
        'products': products,
        'categories': categories,
    }
    return render(req, 'store/index.html', context)


def products(req):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    query = req.GET.get('query') if req.GET.get('query') != None else ''
    products = Product.objects.filter(
        Q(name__icontains=query)
        | Q(brand__icontains=query)
        | Q(category__name__icontains=query)
        | Q(subcategory__name__icontains=query),
    ).distinct().order_by('name')
    objects = paginate_objects(req, products)
    
    context = {
        "products_page": "active",
        'title': 'Products',
        'products': products,
        'objects': objects,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(req, 'store/products.html', context)


def products_grid(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'store/partials/products_grid.html', context)


def product_details(req, pk):
    curr_obj = Product.objects.get(id=pk)
    rel_orders = Product.objects.filter(
        category=curr_obj.category).exclude(id=pk)[:4]
    context = {
        "products_page": "active",
        'title': 'Products',
        'curr_obj': curr_obj,
        'rel_orders': rel_orders,
    }
    return render(req, 'store/prod_details.html', context)


# --------------------------Cart--------------------------

@login_required(login_url='login')
def cart(req):
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()
    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(req, 'store/cart.html', context)

@login_required(login_url='login')
def cart_items_partial(req):
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()
    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(req, 'store/partials/cart_items.html', context)

@login_required(login_url='login')
def add_to_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        print(product_id)
        product = get_object_or_404(Product, id=product_id)
        cart.add_item(product)
        cart_count = len(cart)
        res = JsonResponse({'cart_count': cart_count})
        return res
    
@login_required(login_url='login')
def remove_from_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        # Save to a session
        cart.remove_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res
    
@login_required(login_url='login')
def clear_from_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        # Save to a session
        cart.clear_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res
    
@login_required(login_url='login')
def clear_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        # Save to a session
        cart.clear_cart()
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res

# --------------------------Checkout--------------------------

@login_required(login_url='login')
def checkout(req):
    cart = Cart(req)
    cart_count = len(cart)

    if cart_count == 0:
        messages.info(req, "Access denied: Your cart is empty.")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()
    shipping_info = ShippingInfo.objects.filter(user=req.user).first()
    form = ShippingInfoForm(req.POST or None, instance=shipping_info)

    # Adding new shipping info
    if req.method == 'POST':
        if form.is_valid():
            shipping_info = form.save(commit=False)
            shipping_info.user = req.user
            shipping_info.save()
            messages.success(req, 'Nouvelle info de livraison ajoutée!')
            return redirect('checkout')

    context = {
        "checkout_page": "active",
        'title': 'Checkout',
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_info': shipping_info,
        'form': form,
    }
    return render(req, 'store/checkout.html', context)

# --------------------------Orders--------------------------


@login_required(login_url='login')
def orders(req):
    user = req.user
    min_date_query = req.GET.get('min_date')
    max_date_query = req.GET.get('max_date')
    phone_query = req.GET.get('phone')
    amount_query = req.GET.get('amount')
    items_query = req.GET.get('items')
    status_query = req.GET.get('status')

    if not user.is_staff:
        base_query = Order.objects.filter(user=user).order_by('-timestamp')
    else:
        base_query = Order.objects.all().order_by('-timestamp')

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
    objects = paginate_objects(req, orders)

    context = {
        "orders_page": "active",
        'title': 'Orders',
        "objects": objects,  # Use paginated objects here
    }
    return render(req, 'store/orders.html', context)

def orders_list(req):
    user = req.user
    if not user.is_staff:
        orders = Order.objects.filter(client=user).order_by('-timestamp')
    else:
        orders = Order.objects.all().order_by('-timestamp')
    context = {
        'orders': orders,
    }
    return render(req, 'store/partials/orders_list.html', context)

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
        base_query = Order.objects.filter(user=user).order_by('-timestamp')
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

    return render(req, 'store/partials/orders_list.html', context)

def order_details(req, pk):
    curr_order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order = curr_order)
    rel_orders = Order.objects.filter(
        client=curr_order.client).order_by('-timestamp').exclude(id=pk)[:4]
    context = {
        "order_details": "active",
        'title': 'Order Details',
        'curr_order': curr_order,
        'order_items': order_items,
        'rel_orders': rel_orders,
    }
    return render(req, 'store/order_details.html', context)

@login_required(login_url='login')
def place_order(req):
    user = req.user
    cart = Cart(req)
    cart_items = cart.get_cart_items()
    cart_count = len(cart)
    total_price = cart.get_total_price()

    if cart_count > 0:
        shipping_info = ShippingInfo.objects.filter(user=user).first()
        if not shipping_info:
            messages.error(
                req, "Please provide shipping information before placing an order.")
            return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

        # Create a new order
        new_order = Order(client=user, items=cart_count, amount=total_price)
        new_order.save()
        messages.success(req, 'Nouvelle commande placée!')

        # Create order items
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            price = product.promo_price if product.is_promoted else product.price

            new_order_item = OrderItem(
                order=new_order,
                product=product,
                quantity=quantity,
                price=price * quantity,
            )
            new_order_item.save()

        # Clear the cart after placing the order
        cart.clear_cart()

        return redirect('orders')
    else:
        messages.info(req, "Access denied: Your cart is empty.")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

def cancel_order(req, pk):
    user = req.user
    curr_order = Order.objects.get(id=pk)
    curr_order.status = 'cancelled'
    curr_order.save()

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


# --------------------------Deliveries--------------------------

@login_required(login_url='login')
def deliveries(req):
    user = req.user
    context = {
        "deliveries_page": "active",
        'title': 'deliveries',
    }
    return render(req, 'store/deliveries.html', context)

def deliveries_list(req):
    user = req.user
    if not user.is_staff:
        deliveries = Delivery.objects.filter(client=user).order_by('-timestamp')
    else:
        deliveries = Delivery.objects.all().order_by('-timestamp')
    context = {
        'deliveries': deliveries,
    }
    return render(req, 'store/partials/deliveries_list.html', context)

def postpone_delivery(req, pk):
    user = req.user
    curr_order = Delivery.objects.get(id=pk)
    curr_order.eta = 'cancelled'
    curr_order.save()

def delivery_details(req, pk):
    curr_delivery = Delivery.objects.get(id=pk)
    curr_order = Order.objects.get(id=curr_delivery.id)
    order_items = OrderItem.objects.filter(order=curr_order)
    rel_deliveries = Delivery.objects.filter(
        client=curr_delivery.client).order_by('-timestamp').exclude(id=pk)[:4]
    context = {
        "order_details": "active",
        'title': 'Order Details',
        'curr_order': curr_order,
        'order_items': order_items,
        'rel_deliveries': rel_deliveries,
    }
    return render(req, 'store/delivery_details.html', context)

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
        base_query = Delivery.objects.filter(client=user).order_by('-timestamp')
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

    return render(req, 'store/partials/deliveries_list.html', context)
