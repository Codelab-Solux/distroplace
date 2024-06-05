from calendar import calendar
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.hashers import check_password

from store.cart import *
from store.models import *
from .forms import * # type: ignore
from .models import *
from datetime import datetime


def loginView(req):
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            if 'next' in req.POST:
                return redirect(req.POST.get('next'))

            else:
                return redirect('home')
        else:
            messages.error(req, 'Email ou Mots de passe incorrect!!!')
    context = {
        "login_page": "active",
        "title": 'Login'}
    return render(req, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(req):
    logout(req)
    return redirect('home')


def signupView(req):
    if req.user.is_authenticated:
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            messages.success(req, "Votre compte vien d'être créé.")
            messages.add_message(
                req, messages.SUCCESS, 'Nous venons de vous envoyer un mail pour verifier votre compte')
            return redirect('verify')

        # send_verification_email(req, user)

    context = {
        "signup_page":  "active",
        "title":  'signup',
        'form':  form,
    }
    return render(req, 'accounts/signup.html', context)


@login_required(login_url='login')
def clients_list(req):
    clients = CustomUser.objects.filter(role__id=1)
    context = {
        'clients': clients,
    }
    return render(req, 'accounts/partials/clients_list.html', context)

@login_required(login_url='login')
def staff_list(req):
    staff = CustomUser.objects.filter(role__id__gt=1)
    context = {
        'staff': staff,
    }
    return render(req, 'accounts/partials/staff_list.html', context)


@login_required(login_url='login')
def my_profile(req):
    curr_obj = req.user
    # 
    cart = Cart(req)
    cart_count = len(cart)
    cart_count = 0
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()

    orders = Order.objects.filter(client=curr_obj)
    deliveries = Delivery.objects.filter(client=curr_obj)

    context = {
        "profile_page":"active",
        "curr_obj": curr_obj,
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_price": total_price,
        "orders": orders,
        "deliveries": deliveries,
    }
    return render(req, 'accounts/user_profile.html', context)


@login_required(login_url='login')
def user_profile(req, pk):
    user = req.user
    curr_obj = CustomUser.objects.get(id=pk)
    # 
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()


    context = {
        "profile_page":"active",
        "curr_obj": curr_obj,
        "curr_obj": curr_obj,
        "curr_obj": curr_obj,
    }
    return render(req, 'accounts/user_profile.html', context)
