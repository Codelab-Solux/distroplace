"""
ASGI config for distroplace project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# from whitenoise import WhiteNoise
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distroplace.settings')


application = get_asgi_application()

# application = WhiteNoise(application)
