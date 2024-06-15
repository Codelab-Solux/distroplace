from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('login/google/', google_login, name='google_login'),
    path('logout/', logoutUser, name='logout'),
    path('users/<hashid:pk>/', user_profile, name='user_profile'),
    path('users/my_profile/', my_profile, name='my_profile'),
    path('debug/', debug_view, name='debug_view'),  # Temporary debug view
]
