# Generated by Django 4.2 on 2024-08-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_blogpost_image_alter_promotion_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default='/static/imgs/blog.png', upload_to='base/blogposts/'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='image',
            field=models.ImageField(default='/static/imgs/promo.png', upload_to='base/promotions/'),
        ),
    ]
