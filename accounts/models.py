from phonenumber_field.modelfields import PhoneNumberField
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from datetime import date
from django.utils import timezone
from utils import h_encode, h_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


class Role(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    description = models.TextField(default='', null=True, blank=True)
    sec_level = models.IntegerField(default='0')

    def get_hashid(self):
        return h_encode(self.id)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be prvided')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        db_index=True, unique=True, blank=True, null=True)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email.split("@")[0]}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_short_name(self):
        return f' {self.email.split("@")[0]}'

    def get_full_name(self):
        return f' {self.last_name} {self.first_name}'

    def send_verification_email(self):
        token = default_token_generator.make_token(self)
        uid = self.pk
        url = reverse('verify_email', kwargs={'uid': uid, 'token': token})
        full_url = f'{settings.SITE_URL}{url}'
        send_mail(
            'Verify your email address',
            f'Please verify your email by clicking the following link: {full_url}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
        )


gender_list = (
    ('female', 'Féminin'),
    ('male', 'Masculin'),
)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sex = models.CharField(
        max_length=10, choices=gender_list, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    saved_cart = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='users/profiles', blank=True, null=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} - Profile'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class UserFirebaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firebase_uid = models.CharField(max_length=255, unique=True)
