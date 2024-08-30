from django.db.models.signals import post_migrate, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.apps import apps
from .models import *


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == 'your_app_name':  # Replace 'your_app_name' with your actual Django app name
        # Replace 'your_app_name' with your actual Django app name
        Role = apps.get_model('your_app_name', 'Role')
        if not Role.objects.filter(name='Admin').exists():
            Role.objects.create(
                name='Admin', description='Administrator Role', sec_level=1)
        if not Role.objects.filter(name='Manager').exists():
            Role.objects.create(
                name='Manager', description='Manager Role', sec_level=1)
        if not Role.objects.filter(name='Staff').exists():
            Role.objects.create(
                name='Staff', description='Staff Role', sec_level=1)
        if not Role.objects.filter(name='User').exists():
            Role.objects.create(
                name='User', description='Regular User Role', sec_level=0)
        # Add more roles as needed


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
