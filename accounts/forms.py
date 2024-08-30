from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"
        self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"
        self.fields['password1'].label = "Mot de pass"
        self.fields['password2'].label = "Confirmez votre mot de pass"

    class Meta:
        model = CustomUser
        fields = (
            # 'last_name',
            # 'first_name',
            'email',
            'password1',
            'password2',
        )
        labels = {
            'email': 'Email',
            'first_name': 'Prenoms',
            'last_name': 'Nom',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }

        def clean(self, *args, **kwargs):
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            email_check = CustomUser.objects.filter(email=email)
            if email_check.exists():
                raise forms.ValidationError('This Email already exists')
            if len(password) < 5:
                raise forms.ValidationError(
                    'Your password should have more than 5 characters')
            return super(SignupForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        # Automatically populate first_name and last_name from email (example logic)
        if user.email:
            # Simple logic, customize as needed
            user.first_name = user.email.split('@')[0]
            user.last_name = "_"  # Default value, adjust as needed
        if commit:
            user.save()
        return user


class AltSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'last_name',
            'first_name',
            'phone',
        )
        labels = {
            'first_name': 'Prenoms',
            'last_name': 'Nom',
            'phone': 'Téléphone',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }

    def clean(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                'This phone number is already registered.')
        return super(AltSignupForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        user = super(AltSignupForm, self).save(commit=False)
        user.username = user.phone  # Set the username as the phone number
        user.email = ""  # Set email to an empty string if it's not required
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

        if user and not user.is_superuser:
            self.fields.pop('role')

    class Meta:
        model = CustomUser
        fields = (
            'last_name',
            'first_name',
            'username',
            'email',
            'phone',
            'role',
        )
        labels = {
            'email': 'Email',
            'first_name': 'Prenoms',
            'last_name': 'Nom',
            'username': "Nom d'utilisateur",
            'phone': 'Téléphone',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'role': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        # if user and user.role.sec_level < 3:
        #     self.fields.pop('')

    class Meta:
        model = Profile
        fields = (
            'sex',
            'image',
        )
        labels = {
            'sex': 'Sexe',
            'image': 'Photo de profile',
        }
        widgets = {
            'sex': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-full border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }
