from bot.models import (
    User
)

from bot_helper_py import utils

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)

def handler(name: str):
    return CommandHandler(name, list)

def list(update: Update, _: CallbackContext):
    update.message.reply_text(utils.list_all(User.byUpdate(update).categories.all()))