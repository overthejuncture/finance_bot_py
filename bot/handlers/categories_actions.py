from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bot_helper_py import bot as utils
from bot_helper_py import callback_query as callback_helper
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

from bot.models import (
    User
)

import json

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, categories_actions)],
        states= {
            0: [CallbackQueryHandler(button_click)]
        },
        fallbacks=[],
        allow_reentry=True
    )

def categories_actions(update: Update, context: CallbackContext):
    text, reply_markup = utils.list_with_keyboard(
        User.byUpdate(update).categories.all(),
        field=lambda x: x.name
    )
    update.message.reply_text(text=text, reply_markup=reply_markup)
    return 0

def button_click(update: Update, context: CallbackContext):
    if callback_helper.is_pager_action(update.callback_query):
        start, limit = utils.proccess_pager(update)
    
    text, reply_markup = utils.list_with_keyboard(User.byUpdate(update).categories.all(), start=start, limit=limit)
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    pass