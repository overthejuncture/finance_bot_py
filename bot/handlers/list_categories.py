from bot.models import (
    User,
    Category
)

from bot_helper_py import bot as utils

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)

def handler(name: str):
    return CommandHandler(name, list)

def list(update: Update, context: CallbackContext):
    update.message.reply_text(utils.listAll(User.byUpdate(update).categories.all()))