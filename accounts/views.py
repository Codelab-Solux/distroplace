from django.utils.encoding import force_str
from django.conf import settings
from firebase_admin import auth
import firebase_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from distroplace.backends import FirebaseBackend
from store.cart import *
from store.models import *
from .forms import *
from .models import *
from utils import *


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Your account has been activated successfully!')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('signup')



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
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()
            send_verification_email(req, user)
            messages.success(req, "Votre compte vien d'être créé.")
            messages.add_message(
                req, messages.SUCCESS, 'Nous venons de vous envoyer un mail pour verifier votre compte')
            return redirect('login')

    context = {
        "signup_page":  "active",
        "title":  'signup',
        'form':  form,
    }
    return render(req, 'accounts/signup.html', context)


@login_required(login_url='login')
def user_profile(req, pk):
    user = req.user
    curr_obj = CustomUser.objects.get(id=pk)

    context = {
        "profile_page":"active",
        "curr_obj": curr_obj,
    }
    return render(req, 'accounts/user_profile.html', context)

@login_required(login_url='login')
def my_profile(req):
    curr_obj = req.user
    shipping_info = ShippingInfo.objects.filter(user=curr_obj).first()

    context = {
        "profile_page":"active",
        "curr_obj": curr_obj,
        "shipping_info": shipping_info,
    }
    return render(req, 'accounts/user_profile.html', context)

@login_required(login_url='login')
def user_favorites(req):
    user = req.user
    products = Product.objects.filter(likes=user)

    context = {
        "profile_page":"active",
        "products": products,
    }
    return render(req, 'accounts/partials/user_favorites.html', context)


# ---------------------------------------- Login ----------------------------------------
def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(
                    request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    send_verification_email(request, user)
                    messages.warning(
                        request, "Votre compte n'est pas encore activé. Un nouvel email d'activation vous a été envoyé.")
                    return redirect('login')
            else:
                messages.error(
                    request, 'Nom d\'utilisateur ou mot de passe incorrect.')

        except CustomUser.DoesNotExist:
            messages.error(request, 'Aucun utilisateur touvé')

    return render(request, 'accounts/login.html', {'login_page': 'active', 'title': 'Login'})


# ---------------------------------------- firebase/OTP login views----------------------------------------

def firebase_config(request):
    config = {
        "apiKey": settings.FIREBASE_API_KEY,
        "authDomain": settings.FIREBASE_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_PROJECT_ID,
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
        "appId": settings.FIREBASE_APP_ID,
    }
    return JsonResponse(config)

@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        firebase_token = request.POST.get('firebase_token')
        backend = FirebaseBackend()
        user = backend.authenticate(request, firebase_token=firebase_token)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'}, status=401)
    return JsonResponse({'status': 'bad_request'}, status=400)


def verify_email(request, uid, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'email_verification_failed.html')

