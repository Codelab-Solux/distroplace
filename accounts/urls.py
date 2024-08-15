from django.urls import path, include, register_converter
from .views import *
from utils import HashIdConverter
from django.contrib.auth import views as auth_views

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    # accounts URLs
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/my_profile/', my_profile, name='my_profile'),
    path('users/user_favorites/', user_favorites, name='user_favorites'),
    path('users/activate/<uidb64>/<token>/', activate, name='activate'),
    path('users/<hashid:pk>/', user_profile, name='user_profile'),
    path('verify-email/<uid>/<token>/', verify_email, name='verify_email'),
    path('firebase-login/', firebase_login, name='firebase_login'),
    path('firebase-config/', firebase_config, name='firebase_config'),

    # password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # allauth URLs
    path('', include('allauth.urls')),

]
