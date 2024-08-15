# distroplace/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from firebase_admin import auth

User = get_user_model()


class FirebaseBackend(BaseBackend):
    def authenticate(self, request, firebase_token=None, **kwargs):
        try:
            decoded_token = auth.verify_id_token(firebase_token)
            phone_number = decoded_token.get('phone_number')
            if phone_number:
                try:
                    user = CustomUser.objects.get(phone=phone_number)
                except CustomUser.DoesNotExist:
                    user = CustomUser.objects.create(phone=phone_number)
                    user.set_unusable_password()
                    user.save()
                return user
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
