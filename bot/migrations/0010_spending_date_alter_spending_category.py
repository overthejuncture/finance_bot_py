# Generated by Django 4.0.5 on 2022-07-01 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_remove_spending_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='spending',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spendings', to='bot.category'),
        ),
    ]