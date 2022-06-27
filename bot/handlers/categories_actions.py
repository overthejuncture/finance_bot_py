from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
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
    user = User.byUpdate(update)
    cats = user.categories.all()
    buttons = [
        InlineKeyboardButton(text='1', callback_data='1'),
        InlineKeyboardButton(text='2', callback_data='2'),
    ]
    # reply_markup = InlineKeyboardMarkup(utils.build_menu(buttons=buttons, n_cols=1))
    text, reply_markup = utils.list_with_keyboard(cats, lambda x: x.name)
    update.message.reply_text(text=text, reply_markup=reply_markup)
    pass