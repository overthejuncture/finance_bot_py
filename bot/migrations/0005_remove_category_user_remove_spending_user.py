# Generated by Django 4.0.5 on 2022-06-24 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_spending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.RemoveField(
            model_name='spending',
            name='user',
        ),
    ]