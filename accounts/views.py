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
# from .forms import *
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
    return redirect('login')


def clients_list(req):
    clients = CustomUser.objects.filter(role__id=1)
    context = {
        "customers": "active",
        'title': 'Customers',
        'clients': clients,
    }
    return render(req, 'accounts/partials/clients_list.html', context)
