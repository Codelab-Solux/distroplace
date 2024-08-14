from .models import *
from django import forms
from django.forms import ModelForm


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ('title', 'subtitle','content')
        labels = {'title': 'Titre', 'subtitle': 'Sous-titre', 'content':'Contenu' }
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'subtitle': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'content': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),

        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('comment',)
        labels = {'comment':'Commentaire',}
        widgets = {
            'comment': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ('title', 'catch_phrase', 'price', 'is_active')
        labels = {
            'title':'Titre',
            'catch_phrase': "Phrase d'accroche",
            'price': 'Prix minimum',
            'is_active': 'En cours',
            }
        widgets = {
            'title': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'catch_phrase': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-full border focus:border-none focus:outline-none focus:ring-1 focus:ring-teal-400 w-full"}),
        }

