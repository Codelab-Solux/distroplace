from .models import *
from django import forms
from django.forms import ModelForm


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        labels = {'name': 'Nom', }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-700 w-full"}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ('__all__')
        labels = {'name': 'Nom', 'category': 'Catégorie', }
        widgets = {
            'category': forms.Select(attrs={ 'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-700 w-full"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        labels = {
            'article': 'Nom',
            'brand': 'Marque',
            'category': 'Catégorie',
            'subcategory': "Sous Catégorie",
            'unit': "Unité de mesure",
            'quantity': "Quantité",
            'price': "Prix",
            'promo_price': "Prix de promo",
            'is_expirable': "Périssable",
            'is_promoted': "En Promo",
            'production_date': "Date de production",
            'expiration_date': "Date de péremption",
        }
        widgets = {
            'article': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'category': forms.Select(attrs={ 'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'subcategory': forms.Select(attrs={ 'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'unit': forms.Select(attrs={ 'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'promo_price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'production_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),
            'expiration_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-yellow-400 w-full"}),

        }


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ('__all__')
        exclude = ('user',)

        labels = {
            'phone': 'Telephone',
            'address': 'Adresse',
            'district': 'Quartier',
        }
        widgets = {

            'phone': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-yellow-100 focus:ring-1 focus:ring-yellow-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-yellow-100 focus:ring-1 focus:ring-yellow-400 w-full"}),
            'district': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-yellow-100 focus:ring-1 focus:ring-yellow-400 w-full"}),
        }
