from .models import *
from django import forms
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ('title', 'subtitle', 'content', 'image')
        labels = {'title': 'Titre',
                  'subtitle': 'Sous-titre', 'content': 'Contenu'}
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'subtitle': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            # 'content': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'content': CKEditor5Widget(),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('comment',)
        labels = {'comment': 'Commentaire', }
        widgets = {
            'comment': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ('title', 'catch_phrase', 'price', 'is_active')
        labels = {
            'title': 'Titre',
            'catch_phrase': "Phrase d'accroche",
            'price': 'Prix minimum',
            'is_active': 'En cours',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'catch_phrase': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class HomeImageForm(forms.ModelForm):
    class Meta:
        model = HomeImage
        fields = ('title', 'catch_phrase', 'is_active')
        labels = {
            'title': 'Titre',
            'catch_phrase': "Phrase d'accroche",
            'is_active': 'En vedette',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'catch_phrase': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class ContactMailForm(forms.ModelForm):
    class Meta:
        model = ContactMail
        fields = ('email', 'subject', 'message')
        labels = {
            'email': 'Adresse mail',
            'subject': "Sujet",
            'message': 'Contenu',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'subject': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'message': forms.Textarea(attrs={"rows": "12", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('full_name', 'email', 'products','rating', 'comment')
        labels = {
            'full_name': 'Nom et prénoms',
            'products': 'Produit(s) acheté(s)',
            'rating': 'Note (sur 5)',
            'comment': 'Commentaire',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'products': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-teal-400 w-full"}),
            'rating': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'comment': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


feedback_notes = (
    ('excellent', "Excellent"),
    ('very-good', "Très bon"),
    ('good', "Bon"),
    ('mid', "Moyen"),
    ('bad', "Mauvais"),
)
