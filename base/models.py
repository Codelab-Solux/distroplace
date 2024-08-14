from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from store.models import Product
from utils import h_encode


class Promotion(models.Model):
    title = models.CharField(max_length=255, default='')
    catch_phrase = models.TextField(default='')
    price = models.PositiveBigIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(
        Product, related_name='promotions', blank=True)
    image = models.ImageField(
        upload_to='store/blogposts/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
    content = models.TextField(default='')
    image = models.ImageField(
        upload_to='store/blogposts/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='blogpost_likes', blank=True,)

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
