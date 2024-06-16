from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib import messages
from store.models import *
from .forms import *
from .models import *

# Create your views here.


def home(req):
    latest_posts = Blogpost.objects.all().order_by('-timestamp')[:3]
    appliances = Product.objects.filter(is_featured=True, category__id=1)
    fruits_veggies_spices = Product.objects.filter(
        is_featured=True
    ).filter(
        Q(category__id=4) | Q(category__id=5) | Q(category__id=8)
    )
    spices = Product.objects.filter(is_featured=True, category__id=8)
    cloths = Product.objects.filter(is_featured=True, category__id=10)
    categories = Category.objects.filter(is_featured=True)
    subcategories = SubCategory.objects.all()
    active_promos = Promotion.objects.filter(is_active=True)[:3]
    # Ensure there are at least three promotions in the database
    if len(active_promos) >= 3:
        promo_1 = active_promos[0]  # First promotion in the queryset
        promo_2 = active_promos[1]  # Second promotion in the queryset
        promo_3 = active_promos[2]  # Third promotion in the queryset
    else:
        # Handle case where there are fewer than 3 promotions in the database
        active_promos = None
        promo_1 = None
        promo_2 = None
        promo_3 = None
    context = {
        "home_page": "active",
        'title': 'Store',
        'appliances': appliances,
        'fruits_veggies_spices': fruits_veggies_spices,
        'spices': spices,
        'cloths': cloths,
        'categories': categories,
        'subcategories': subcategories,
        'latest_posts': latest_posts,
        'active_promos': active_promos,
        'promo_1': promo_1,
        'promo_2': promo_2,
        'promo_3': promo_3,
    }
    return render(req, 'base/index.html', context)

def blog(req):
    blogposts = Blogpost.objects.all().order_by('-timestamp')
    context = {
        "blog_page": "active",
        'title': 'Store',
        'blogposts': blogposts,
    }
    return render(req, 'base/blog.html', context)


def blogpost(req, pk):
    print(pk)
    curr_obj = get_object_or_404(Blogpost, id=pk)
    query = req.GET.get('query') if req.GET.get('query') != None else ''
    blogposts = Blogpost.objects.filter(
        Q(title__icontains=query)
        | Q(subtitle__icontains=query)
    ).order_by('-timestamp').exclude(id=curr_obj.id)[:4]

    context = {
        "blogpost_page": "active",
        'title': 'Blogpost details',
        'curr_obj': curr_obj,
        'blogposts': blogposts,

    }

    return render(req, 'base/blogpost.html', context)


@login_required(login_url='login')
def add_blogpost(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = BlogForm()
    if req.method == 'POST':
        form = BlogForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Nouveau produit ajouté')
            return redirect('blog')

    else:
        return render(req, 'base/blog_form.html', context={
            'title': 'Products', 'form': form, 'form_title': 'Nouvel article'})


# --------------------------newsletter--------------------------
def mailing_list(req):
    emails = NewsletterEmails.objects.all().order_by('-email')
    context = {
        'emails': emails,
    }
    return render(req, 'base/partials/email_list.html', context)


# --------------------------Promotions--------------------------
def promotions(req):
    promotions = Promotion.objects.filter(
        is_active=True).order_by('-timestamp')
    context = {
        "promotions_page": "active",
        'title': 'Promotions',
        'promotions': promotions,
    }
    return render(req, 'base/promotions.html', context)



def promo_details(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    products = promotion.products.all()
    context = {
        "promo_page": "active",
        'title': 'Promo Details',
        'promotion': promotion,
        'products': products,
    }
    return render(request, 'base/promo_details.html', context)


# --------------------------Promotions--------------------------


def privacy_policy(req):
    context = {
        "privacy_policy_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/privacy_policy.html', context)

def terms_of_use(req):
    context = {
        "terms_of_use_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/terms_of_use.html', context)

def delivery_policy(req):
    context = {
        "delivery_policy_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/delivery_policy.html', context)

def return_policy(req):
    context = {
        "return_policy_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/return_policy.html', context)

def feedbacks(req):
    context = {
        "feedbacks_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/feedbacks.html', context)

def about(req):
    context = {
        "about_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/about.html', context)

def contact(req):
    context = {
        "contact_page": "active",
        "title": 'Privacy Policy',
    }
    return render(req, 'base/extras/contact.html', context)


def not_found(req, exception):
    context = {
        "not_found_page": "active",
        "title": 'Page 404',

    }
    return render(req, 'base/extras/not_found.html', context)
