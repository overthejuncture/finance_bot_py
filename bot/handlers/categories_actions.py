from subprocess import call
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
    Category,
    User
)

from typing import List

import json

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, categories_actions)],
        states= {
            0: [CallbackQueryHandler(button_click_action)],
            1: [CallbackQueryHandler(apply_category_action)]
        },
        fallbacks=[],
        run_async=True,
        allow_reentry=True
    )

def categories_actions(update: Update, context: CallbackContext):
    text, reply_markup = utils.list_with_keyboard_and_pager(
        User.byUpdate(update).categories.all(),
        field=lambda x: x.name
    )
    update.message.reply_text(text=text, reply_markup=reply_markup)
    return 0

def button_click_action(update: Update, context: CallbackContext):
    if callback_helper.is_pager_action(update.callback_query):
        start, limit = utils.proccess_pager(update)
        text, reply_markup = utils.list_with_keyboard_and_pager(User.byUpdate(update).categories.all(), start=start, limit=limit)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        return 0
    
    data = json.loads(update.callback_query.data)
    send_category_actions(update, data.get('data').get('id'))
    return 1

def send_category_actions(update: Update, id: int):
    cat = Category.objects.get(pk=id)
    update.callback_query.message.reply_text(
        text=cat.name,
        reply_markup=InlineKeyboardMarkup(utils.create_action_buttons(data={'id': id}, edit=True, delete=True))
    )

def apply_category_action(update: Update, context: CallbackContext):
    data = json.loads(update.callback_query.data)
    action = callback_helper.get_action(update.callback_query)
    print(data)