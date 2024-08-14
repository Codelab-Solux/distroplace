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


# ---------------------------------------- Login views----------------------------------------
def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')

        try:
            # Check if the input is an email
            if '@' in email_or_phone:
                user = authenticate(
                    request, email=email_or_phone, password=password)
            else:
                # Assume it's a phone number and look up the user by phone
                user = CustomUser.objects.get(phone=email_or_phone)
                user = authenticate(
                    request, email=user.email, password=password)

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


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        verification_id = request.session.get('verification_id')
        user_id = request.session.get('otp_user_id')

        if not user_id:
            messages.error(request, 'Session expired or invalid.')
            return redirect('login')

        try:
            user = CustomUser.objects.get(id=user_id)
            if verification_id and otp:
                try:
                    # Verify the OTP using Firebase
                    # credentials = auth.verify_phone_number(
                    #     verification_id, otp)
                    login(request, user)
                    del request.session['verification_id']
                    del request.session['otp_user_id']
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f"Error verifying OTP: {e}")
                    return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid session or user does not exist.')

    return render(request, 'accounts/otp.html')


def resend_otp(request):
    user_id = request.session.get('otp_user_id')

    if not user_id:
        messages.error(request, 'Session expired or invalid.')
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
        # Ensure the phone number format is correct
        phone_number = f"+{user.phone}"

        # Send a new OTP using Firebase
        try:
            verification = auth.send_verification_code(phone_number)
            request.session['verification_id'] = verification['sessionInfo']
            messages.success(request, 'A new OTP has been sent to your phone.')
            return redirect('verify_otp')
        except Exception as e:
            messages.error(request, f"Error sending OTP: {e}")
            return redirect('verify_otp')

    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid session or user does not exist.')
        return redirect('login')


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


# ---------------------------------------- firebase/OTP login views----------------------------------------
@csrf_exempt
def firebase_auth(request):
    if request.method == 'POST':
        id_token = request.POST.get('idToken')
        try:
            decoded_token = auth.verify_id_token(id_token)
            phone_number = decoded_token['phone_number']
            uid = decoded_token['uid']

            # Check if the user already exists
            user, created = CustomUser.objects.get_or_create(
                phone=phone_number)

            if created:
                user.username = uid  # You can customize how you want to set the username
                user.save()

            # Log the user in
            login(request, user)
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def firebase_config(request):
    config = {
        "apiKey": settings.FIREBASE_API_KEY,
        "authDomain": settings.FIREBASE_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_PROJECT_ID,
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
        "appId": settings.FIREBASE_APP_ID,
        "measurementId": settings.FIREBASE_MEASUREMENT_ID,
    }
    return JsonResponse(config)


