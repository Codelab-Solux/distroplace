from .models import *
from django import forms
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        labels = {'name': 'Nom', 'is_featured': 'En vedette'}
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ('__all__')
        labels = {'name': 'Nom', 'category': 'Catégorie', }
        widgets = {
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

        labels = {
            'name': 'Article',
            'thumbnail': 'Image de couverture',
            'brand': 'Marque',
            'category': 'Catégorie',
            'subcategory': "Sous Catégorie",
            'unit': "Unité de mesure",
            'quantity': "Quantité",
            'price': "Prix",
            'supplier': "Fournisseur",
            'promo_price': "Prix de promo",
            'is_expirable': "Périssable",
            'is_promoted': "En Promo",
            'is_new': "Nouvel arrivage",
            'production_date': "Date de production",
            'expiration_date': "Date de péremption",
        }


        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'subcategory': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'unit': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'promo_price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'description': CKEditor5Widget(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'production_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'expiration_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),

        }

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['subcategory'].queryset = SubCategory.objects.none()

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = SubCategory.objects.filter(
                        category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty SubCategory queryset
            elif self.instance.pk:
                self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by(
                    'name')


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

            'phone': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-teal-100 focus:ring-1 focus:ring-teal-400  w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-teal-100 focus:ring-1 focus:ring-teal-400  w-full"}),
            'district': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-teal-100 focus:ring-1 focus:ring-teal-400  w-full"}),
        }


class DeliveryTypeForm(forms.ModelForm):
    class Meta:
        model = DeliveryType
        fields = '__all__'

        labels = {
            'title': 'Nom',
            'price': 'Prix',
            'eta': 'Délais',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'price': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'eta': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

        labels = {
            'name': 'Nom',
            'phone': 'Telephone',
            'address': 'Adresse',
            'domain': 'Secteur',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('comment',)
        labels = {'comment': 'Commentaire', }
        widgets = {
            'comment': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }
