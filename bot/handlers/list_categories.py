from bot.models import (
    User,
    Category
)

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)

def handler(name: str):
    return CommandHandler(name, list)

def list(update: Update, context: CallbackContext):
    cats = Category.objects.filter(user=User.byUpdate(update))
    to_return = "\n".join("{idx}. {name}".format(idx=idx+1, name=cat.name) for idx, cat in enumerate(cats))
    update.message.reply_text(to_return)