from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField()
