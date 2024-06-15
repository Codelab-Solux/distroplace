# Generated by Django 4.2 on 2024-06-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_delivery_delivery_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_favorite',
        ),
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]