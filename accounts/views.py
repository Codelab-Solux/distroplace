from django.utils.encoding import force_str
from django.conf import settings
from firebase_admin import auth
import firebase_admin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.signals import create_profile
from distroplace.backends import FirebaseBackend
from store.cart import *
from store.forms import ShippingInfoForm
from store.models import *
from .forms import *
from .models import *
from utils import *


def signupView(req):
    if req.user.is_authenticated:
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False  # Deactivate account until email confirmation
            user.save()
            send_verification_email(req, user)
            messages.success(req, "Votre compte vien d'être créé.")
            messages.add_message(
                req, messages.SUCCESS, 'Nous venons de vous envoyer un mail pour vérifier votre compte')
            return redirect('login')
        
    # alt_form = AltSignupForm()
    # if req.method == 'POST':
    #     alt_form = AltSignupForm(req.POST)
    #     if alt_form.is_valid():
    #         user = alt_form.save(commit=False)
    #         user.is_active = False  # Deactivate account until email confirmation
    #         user.save()
    #         # send_verification_sms(req, user)
    #         messages.success(req, "Votre compte vien d'être créé.")
    #         messages.add_message(
    #             req, messages.SUCCESS, 'Nous venons de vous envoyer un sms pour vérifier votre compte')
    #         return redirect('login')

    context = {
        "signup_page":  "active",
        "title":  'signup',
        'form':  form,
        # 'alt_form':  alt_form,
    }
    return render(req, 'accounts/signup.html', context)


def send_verification_email(req, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(req)
    mail_subject = 'Vérifiez votre compte'
    message = render_to_string('accounts/partials/verif_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()


def resend_verif_mail(req, pk):
    user = get_object_or_404(CustomUser, id=pk)
    send_verification_email(req, user)
    messages.info(
        req, 'Nous venons de vous envoyer un nouveau mail de vérification!!!')
    return redirect('login')


def verify_by_email(req, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True  # Activate the user account
        user.save()
        messages.success(req, 'Votre compte a été vérifié avec succès.')
        return redirect('login')
    else:
        return render(req, 'accounts/partials/verif_failed.html', context={'user': user})


# ---------------------------------------- login/logout ----------------------------------------
def loginView(req):
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        try:
            user = authenticate(
                req, email=email, password=password)
            # user = get_object_or_404(CustomUser, email=email)

            if user is not None:
                if user.is_verified:
                    login(req, user)
                    return redirect('home')
                else:
                    send_verification_email(req, user)
                    messages.warning(
                        req, "Votre compte n'est pas encore vérifié. Un nouveau mail de vérification vous a été envoyé.")
                    return redirect('login')
            else:
                messages.error(
                    req, 'Nom d\'utilisateur ou mot de passe incorrect.')

        except CustomUser.DoesNotExist:
            messages.error(req, 'Aucun utilisateur touvé')

    return render(req, 'accounts/login.html', {'login_page': 'active', 'title': 'Login'})


@login_required(login_url='login')
def logoutUser(req):
    logout(req)
    return redirect('home')


# ---------------------------------------- user views ----------------------------------------
@login_required(login_url='login')
def user_profile(req, pk):
    curr_obj = CustomUser.objects.get(id=pk)
    context = {
        "title": "Profile",
        "profile_page": "active",
        "curr_obj": curr_obj,
    }
    return render(req, 'accounts/user_profile.html', context)


@login_required(login_url='login')
def my_profile(req):
    curr_obj = req.user
    context = {
        "title":"Profile",
        "profile_page": "active",
        "curr_obj": curr_obj,
    }
    return render(req, 'accounts/user_profile.html', context)


@login_required(login_url='login')
def user_favorites(req):
    user = req.user
    products = Product.objects.filter(likes=user)
    context = {
        "profile_page": "active",
        "products": products,
    }
    return render(req, 'accounts/partials/user_favorites.html', context)


@login_required(login_url='login')
def user_info(req, pk):
    curr_obj = CustomUser.objects.get(id=pk)
    shipping_info = ShippingInfo.objects.filter(user=curr_obj).first()
    context = {
        "curr_obj": curr_obj,
        "shipping_info": shipping_info,
    }
    return render(req, 'accounts/partials/user_info.html', context)


# ---------------------------------------- firebase/OTP login views----------------------------------------
def firebase_config(req):
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
def firebase_login(req):
    if req.method == 'POST':
        firebase_token = req.POST.get('firebase_token')
        backend = FirebaseBackend()
        user = backend.authenticate(req, firebase_token=firebase_token)
        if user is not None:
            login(req, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'}, status=401)
    return JsonResponse({'status': 'bad_req'}, status=400)


def otp_login(req):
    if req.method == "POST":
        phone_number = req.POST.get('phone')
        # Here you would integrate with Firebase to send OTP
        # You might use the firebase-admin SDK or directly from your frontend
        return JsonResponse({"message": "OTP sent"})

    return render(req, 'accounts/otp_login.html')


def otp_verify(req):
    if req.method == "POST":
        otp = req.POST.get('otp')
        # Verify OTP with Firebase
        try:
            # Use Firebase to verify the OTP
            decoded_token = auth.verify_id_token(otp)
            uid = decoded_token['uid']
            # Log the user in with the obtained UID or create a new user
            return JsonResponse({"message": "OTP verified, user logged in"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return render(req, 'accounts/otp_verify.html')


# ---------------------------------------- user edit views----------------------------------------

@login_required(login_url='login')
def edit_user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)

    if user != curr_obj:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if req.method == 'POST':
        form = EditUserForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            form.save()
            messages.success(req, 'Compte modifié')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        form = EditUserForm(instance=curr_obj, user=user)
    return render(req, 'basic_form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce compte'})



@login_required(login_url='login')
def edit_profile(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Profile, id=pk)

    if user != curr_obj.user:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProfileForm(instance=curr_obj, user=user)
    if req.method == 'POST':
        form = ProfileForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            form.save()
        messages.success = 'Profile modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'basic_form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce profile'})


@login_required(login_url='login')
def manage_shipping_info(req):
    user = req.user
    # Try to retrieve existing shipping info
    try:
        shipping_info = ShippingInfo.objects.get(user=user)
        form = ShippingInfoForm(req.POST or None, instance=shipping_info)
        is_update = True
    except ShippingInfo.DoesNotExist:
        form = ShippingInfoForm(req.POST or None)
        is_update = False

    if req.method == 'POST':
        if form.is_valid():
            form.instance.user = user
            form.save()
            if is_update:
                messages.success(req, 'Infos mises à jour')
            else:
                messages.success(req, 'Infos ajoutées')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

    return render(req, 'basic_form.html', context={
        'form': form,
        'form_title': 'Ajouter ou mettre à jour les infos de livraison',
    })
