# Generated by Django 4.2 on 2024-06-14 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0014_product_is_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('person', 'Individu'), ('company', 'Compagnie')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.supplier'),
        ),
    ]