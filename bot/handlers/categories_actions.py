from subprocess import call
from telegram import (
    Update,
    InlineKeyboardMarkup
)
from bot_helper_py import utils
from bot_helper_py import callback_utils
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

from bot.models import (
    Category,
    User
)

import json

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, categories_actions)],
        states= {
            0: [CallbackQueryHandler(button_click_action)],
            1: [CallbackQueryHandler(apply_category_action)],
            2: [MessageHandler(Filters.text, edit_category)]
        },
        fallbacks=[],
        run_async=True,
        allow_reentry=True
    )

def categories_actions(update: Update, _: CallbackContext):
    text, reply_markup = utils.list_with_keyboard_and_pager(
        User.byUpdate(update).categories.all(),
        field=lambda x: x.name
    )
    update.message.reply_text(text=text, reply_markup=reply_markup)
    return 0

def button_click_action(update: Update, _: CallbackContext):
    if callback_utils.is_pager_action(update.callback_query):
        start, limit = utils.proccess_pager(update)
        text, reply_markup = utils.list_with_keyboard_and_pager(User.byUpdate(update).categories.all(), start=start, limit=limit)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        return 0
    
    data = json.loads(update.callback_query.data)
    _send_category_actions(update, data.get(utils.DATA_LITERAL).get('id'))
    return 1

def _send_category_actions(update: Update, id: int):
    cat = Category.objects.get(pk=id)
    update.callback_query.edit_message_reply_markup()
    update.callback_query.message.reply_text(
        text=cat.name,
        reply_markup=InlineKeyboardMarkup(utils.create_action_buttons(data={'id': id}, edit=True, delete=True))
    )

def apply_category_action(update: Update, context: CallbackContext):
    action, data = callback_utils.get_action(update.callback_query)
    cat = Category.objects.get(pk=data.get('id'))
    update.callback_query.edit_message_reply_markup()
    if action == utils.DELETE_ACTION:
        cat.delete()
        update.callback_query.message.reply_text('Удалено')
        ConversationHandler.END
    
    if action == utils.EDIT_ACTION:
        context.user_data['category'] = cat.pk
        update.callback_query.message.reply_text('Введите новое наименование категории')
        return 2

def edit_category(update: Update, context: CallbackContext):
    cat = Category.objects.get(pk=context.user_data['category'])
    cat.name = update.message.text
    cat.save()
    update.message.reply_text('Обновлено')
    return ConversationHandler.END