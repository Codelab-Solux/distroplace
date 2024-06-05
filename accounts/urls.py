from django.urls import path, register_converter
from . import views
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('clients/', clients_list, name='clients_list'),
    path('users/<hashid:pk>/', user_profile, name='user_profile'),
    path('users/my_profile/', my_profile, name='my_profile'),
    # path('users/', users, name='users'),
    # path('users/new/', create_user, name='create_user'),
    # path('users/<hashid:pk>/profile', profile, name='profile'),
    # path('users/<hashid:pk>/delete', delete_user, name='delete_user'),
    # path('users/<hashid:pk>/edit', edit_user, name='edit_user'),
    # path('profiles/<hashid:pk>/edit', edit_profile, name='edit_profile'),
]


htmx_urls = [
    # path('users/<hashid:pk>/', user, name='user'),
    # path('users/filter/<str:pk>/', filter_users, name='filter_users'),
    # path('users/list/<str:pk>/', users_list, name='users_list'),
    # path('times/records/new/', new_time_record, name='new_time_record'),
    # path('times/records/<hashid:pk>/', recent_moves, name='recent_moves'),
    # path('times/records/<hashid:pk>/', time_records, name='time_records'),

]

urlpatterns += htmx_urls
