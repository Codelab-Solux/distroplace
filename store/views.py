from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
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


def product_details(req, pk):
    user = req.user
    curr_obj = Product.objects.get(id=pk)
    prod_images = ProductImage.objects.filter(product=curr_obj)
    rel_products = Product.objects.filter(
        category=curr_obj.category).exclude(id=pk).order_by('-timestamp')[:4]
    is_favorite = curr_obj.likes.filter(id=user.id).exists()
    context = {
        "products_page": "active",
        'title': 'Products',
        'curr_obj': curr_obj,
        'prod_images': prod_images,
        'rel_products': rel_products,
        'is_favorite': is_favorite,
    }
    return render(req, 'store/prod_details.html', context)


def product_info(req, pk):
    curr_obj = get_object_or_404(Product, id=pk)
    comments = ProductComment.objects.filter(
        product=curr_obj).order_by('-timestamp')
    is_liked = False
    if curr_obj.likes.filter(id=req.user.id).exists():
        is_liked = True

    context = {
        'curr_obj': curr_obj,
        'comments': comments,
        'is_liked': is_liked,
    }

    return render(req, 'store/partials/product_info.html', context)


@login_required(login_url='login')
def make_favorite(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Product, id=pk)

    if curr_obj.likes.filter(id=user.id).exists():
        curr_obj.likes.remove(user)
        is_favorite = False
    else:
        curr_obj.likes.add(user)
        is_favorite = True
    print(is_favorite)
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def like_product(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Product, id=pk)

    if curr_obj.likes.filter(id=user.id).exists():
        curr_obj.likes.remove(user)
        is_liked = False
    else:
        curr_obj.likes.add(user)
        is_liked = True
    print(is_liked)
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

# ----------------------------------------

def create_prod_comment(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Product, id=pk)
    if req.method == 'POST':
        comment = req.POST['comment']
        new_comment = ProductComment(
            product=curr_obj, user=user, comment=comment)
        new_comment.save()

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def edit_prod_comment(req, pk):
    user = req.user
    curr_obj = get_object_or_404(ProductComment, id=pk)

    if not user.is_staff:
        return redirect(req.META.get('HTTP_REFERER', '/'))

    form = ProductCommentForm(instance=curr_obj)
    if req.method == 'POST':
        form = ProductCommentForm(req.POST,  instance=curr_obj)
        if (form.is_valid):
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'form': form, 'form_title': 'Modifier ce commentaire', "curr_obj": curr_obj})

# --------------------------Cart--------------------------

# @login_required(login_url='login')
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

# @login_required(login_url='login')
def cart_partial(req):
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

# @login_required(login_url='login')
def cart_resume(req):
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(req, 'store/partials/cart_resume.html', context)

# @login_required(login_url='login')
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
    
# @login_required(login_url='login')
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
    
# @login_required(login_url='login')
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
    
# @login_required(login_url='login')
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
        base_query = Order.objects.filter(client=user).order_by('-timestamp')
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

def order_details(req, pk):
    curr_obj = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order = curr_obj)
    rel_orders = Order.objects.filter(
        client=curr_obj.client).order_by('-timestamp').exclude(id=pk)[:4]
    delivery_types = DeliveryType.objects.all()

    has_delivery = Delivery.objects.filter(order=curr_obj).first()
    # if not has_delivery:
    #     has_delivery = False


    context = {
        "order_details": "active",
        'title': 'Order Details',
        'curr_obj': curr_obj,
        'order_items': order_items,
        'rel_orders': rel_orders,
        'delivery_types': delivery_types,
        'has_delivery': has_delivery,
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

        return redirect('order_details', pk=new_order.id)
    else:
        messages.info(req, "Access denied: Your cart is empty.")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


def cancel_order(req, pk):
    user = req.user
    curr_order = Order.objects.get(id=pk)
    curr_order.status = 'cancelled'
    curr_order.save()

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def orders_resume(req):
    user = req.user
    orders = Order.objects.filter(client=user)
    pending = orders.filter(status='pending')
    processed = orders.filter(status='processed')
    delivered = orders.filter(status='delivered')
    cancelled = orders.filter(status='cancelled')

    context = {
        "orders": orders,
        "pending": pending,
        "processed": processed,
        "delivered": delivered,
        "cancelled": cancelled,
    }
    return render(req, 'store/partials/orders_resume.html', context)

# --------------------------Deliveries--------------------------

@login_required(login_url='login')
def deliveries(req):
    user = req.user
    min_date_query = req.GET.get('min_date')
    max_date_query = req.GET.get('max_date')
    phone_query = req.GET.get('phone')
    amount_query = req.GET.get('amount')
    items_query = req.GET.get('items')
    status_query = req.GET.get('status')

    if not user.is_staff:
        base_query = Delivery.objects.filter(
            client=user).order_by('-timestamp')
    else:
        base_query = Delivery.objects.all().order_by('-timestamp')

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

    objects = paginate_objects(req, base_query)

    context = {
        "deliveries_page": "active",
        'title': 'deliveries',
        'objects': objects,
    }
    return render(req, 'store/deliveries.html', context)

def new_delivery(req, pk):
    user = req.user
    curr_obj = Order.objects.get(id=pk)
    delivery_type = req.POST.get('delivery_type')
    delivery_type = DeliveryType.objects.get(id=delivery_type)
    delivery_phone = req.POST.get('delivery_phone')
    shipping_info = ShippingInfo.objects.get(user=curr_obj.client)

    if not delivery_phone:
        delivery_phone = shipping_info.phone

    print(delivery_phone)

    new_delivery = Delivery(
        order=curr_obj,
        client=curr_obj.client,
        items=curr_obj.items,
        phone=delivery_phone,
        amount_due=curr_obj.amount,
        delivery_type=delivery_type,
    )

    new_delivery.save()

    # Get the referrer URL
    referrer_url = req.META.get('HTTP_REFERER', '/')

    # Redirect to the referrer URL or a default URL if referrer is not available
    return redirect(referrer_url)


def postpone_delivery(req, pk):
    user = req.user
    curr_obj = Delivery.objects.get(id=pk)
    new_dday = 'Date'
    curr_obj.dday = new_dday
    curr_obj.save()

def delivery_details(req, pk):
    curr_obj = Delivery.objects.get(id=pk)
    curr_order = Order.objects.get(id=curr_obj.order.id)
    order_items = OrderItem.objects.filter(order=curr_order)
    rel_deliveries = Delivery.objects.filter(
        client=curr_obj.client).order_by('-timestamp').exclude(id=pk)[:4]
    shipping_info = ShippingInfo.objects.filter(user=req.user).first()
    
    context = {
        "order_details": "active",
        'title': 'Order Details',
        'curr_obj': curr_obj,
        'curr_order': curr_order,
        'order_items': order_items,
        'rel_deliveries': rel_deliveries,
        'shipping_info': shipping_info,
    }
    return render(req, 'store/delivery_details.html', context)


@login_required(login_url='login')
def deliveries_resume(req):
    user = req.user
    deliveries = Delivery.objects.filter(client=user)
    pending = deliveries.filter(status='pending')
    dispatched = deliveries.filter(status='dispatched')
    finished = deliveries.filter(status='finished')
    cancelled = deliveries.filter(status='cancelled')

    context = {
        "deliveries": deliveries,
        "pending": pending,
        "dispatched": dispatched,
        "finished": finished,
        "cancelled": cancelled,
    }
    return render(req, 'store/partials/deliveries_resume.html', context)

# ------------------------------------------------- Delete and 404 routes -------------------------------------------------


@require_http_methods(['DELETE'])
@login_required(login_url='login')
def delete_store_object(req, pk, model_name):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    try:
        # Get the model class from the model name
        ModelClass = apps.get_model('base', model_name)
    except LookupError:
        return HttpResponse(status=404)  # Model not found

    # Fetch the object to be deleted
    obj = get_object_or_404(ModelClass, pk=pk)

    # Check user's permission and show snackabr
    if req.user.role.sec_level < 2:
        # Send a custom HTMX trigger
        response = HttpResponse(status=403, headers={
                                'HX-Trigger': 'access-denied'})
        return response

    # Delete the object
    obj.delete()

    # Return a success response
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
