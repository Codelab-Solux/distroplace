from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from store.models import Product
from utils import h_encode


class Promotion(models.Model):
    title = models.CharField(max_length=255, default='')
    catch_phrase = models.TextField(default='')
    price = models.PositiveBigIntegerField(default=0)
    products = models.ManyToManyField(
        Product, related_name='promotions', blank=True)
    image = models.ImageField(
        upload_to='base/promotions', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('promotion', kwargs={'pk': self.pk})


class Blogpost(models.Model):
    title = models.CharField(max_length=255, default='')
    subtitle = models.CharField(
        max_length=255, default='', blank=True, null=True)
    content = CKEditor5Field('Content', config_name='extends', blank=True)
    image = models.ImageField(
        upload_to='base/blogposts', blank=True, null=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='blogpost_likes', blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('blogpost', kwargs={'pk': self.pk})


class BlogComment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    blogpost = models.ForeignKey(
        Blogpost, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.blogpost.title} - comment'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('blog_comment', kwargs={'pk': self.pk})


class NewsletterEmails(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('news_letter_email', kwargs={'pk': self.pk})


class HomeImage(models.Model):
    title = models.CharField(max_length=255, default='')
    catch_phrase = models.TextField(default='')
    image = models.ImageField(
        upload_to='base/home_image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('home_image', kwargs={'pk': self.pk})


class ContactMail(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255, default='')
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('contact_mail', kwargs={'pk': self.pk})


class Rating(models.Model):
    title = models.CharField(max_length=255)
    stars = models.IntegerField()

    def __str__(self):
        return f'{self.title} - feedback'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('rating', kwargs={'pk': self.pk})

class Feedback(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    products = models.CharField(max_length=255)
    rating = models.ForeignKey(
            Rating, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - feedback'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('feedback', kwargs={'pk': self.pk})
