# Generated by Django 4.2 on 2024-06-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_supplier_alter_product_likes_product_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default='True'),
        ),
    ]