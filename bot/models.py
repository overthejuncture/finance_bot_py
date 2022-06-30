from functools import total_ordering
from django.db import models
from telegram import Update

class User(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True)

    def __str__(self) -> str:
        return "{id} {telegram_id}".format(id=self.pk, telegram_id=self.telegram_id)

    def byUpdate(update: Update):
        if update.message != None:
            id = update.message.from_user.id
        else:
            id = update.callback_query.from_user.id
        return User.objects.get(pk=id)


class Category(models.Model):
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self) -> str:
        return "ID: {id} Name: {name} User.ID: {user}".format(id=self.pk, name=self.name, user=self.user.pk)

class Spending(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "ID: {id} Amount: {amount} User.ID: {user} Category.ID: {cat}".format(
            id=self.pk, amount=self.amount, user=self.user.pk, cat=self.category.pk)