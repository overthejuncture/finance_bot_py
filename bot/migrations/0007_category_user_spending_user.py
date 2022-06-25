# Generated by Django 4.0.5 on 2022-06-24 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_remove_user_id_alter_user_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bot.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spending',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bot.user'),
            preserve_default=False,
        ),
    ]
