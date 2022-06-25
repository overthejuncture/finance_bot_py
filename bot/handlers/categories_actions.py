from telegram import Update
from bot_helper_py import bot as utils
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)

from bot.models import (
    User
)

def handler(name: str):
    return CommandHandler(name, categories_actions)

def categories_actions(update: Update, context: CallbackContext):
    
    pass