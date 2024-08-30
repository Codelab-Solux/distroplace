# Generated by Django 4.2 on 2024-08-29 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_blogpost_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(default='', max_length=255)),
                ('content', models.TextField(default='')),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='homeimages',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]