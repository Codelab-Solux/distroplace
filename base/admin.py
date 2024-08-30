from django.contrib import admin
from .models import *



class CommentInline(admin.TabularInline):
    model = BlogComment

class BlogAdmin(admin.ModelAdmin):
    inline = [
        CommentInline,
    ]
    list_display = ("title", "timestamp")


# Register your models here.
admin.site.register(Promotion)
admin.site.register(Blogpost, BlogAdmin)
admin.site.register(BlogComment)
admin.site.register(NewsletterEmails)
admin.site.register(HomeImage)
admin.site.register(ContactMail)
admin.site.register(Rating)
admin.site.register(Feedback)

