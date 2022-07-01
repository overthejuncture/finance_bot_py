from bot.models import (
    User
)

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)

def handler(name: str):
    return CommandHandler(name, start)

def start(update: Update, _: CallbackContext):
    id = update.message.from_user.id
    user = User(telegram_id = id)
    user.save()
    update.message.reply_text('Пользователь добавлен')
    pass