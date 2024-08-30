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
    path('users/<hashid:pk>/', user_profile, name='user_profile'),
    path('users/<hashid:pk>/info/', user_info, name='user_info'),
    path('users/resend_verif_mail/<int:pk>/',
         resend_verif_mail, name='resend_verif_mail'),
    path('users/verify_by_email/<uidb64>/<token>/',
         verify_by_email, name='verify_by_email'),
    path('users/<hashid:pk>/edit/', edit_user, name='edit_user'),
    path('users/<hashid:pk>/profile/edit/',
         edit_profile, name='edit_profile'),
    path('firebase-login/', firebase_login, name='firebase_login'),
    path('firebase-config/', firebase_config, name='firebase_config'),
    path('otp_login/', otp_login, name='otp_login'),
    path('otp_verify/', otp_verify, name='otp_verify'),
    path('shipping_info/', manage_shipping_info, name='manage_shipping_info'),

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
