from bot.models import (
    User,
    Category
)

from bot_helper_py import bot as utils, callback_query as callback_helper

from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, start)],
        states={
            0: [CallbackQueryHandler(button_click)]
        },
        fallbacks=[]
    )

def start(update: Update, context: CallbackContext):
    text, r_m = utils.list_with_keyboard_and_pager(User.byUpdate(update).categories.all(), field=lambda x: x.name)
    update.message.reply_text("Выберите категорию\n" + text, reply_markup=r_m)
    return 0

def button_click(update: Update, context: CallbackContext):
    if callback_helper.is_pager_action(update.callback_query):
        start, limit = utils.proccess_pager(update)
        t, r_m = utils.list_with_keyboard_and_pager(User.byUpdate(update).categories.all(), start, limit)
        update.callback_query.edit_message_text(text=t, reply_markup=r_m)
        return 0
    list(update)
    ConversationHandler.END

def list(update: Update):
    data = callback_helper.get_data(update.callback_query)
    id = data.get('id')
    spendings = Category.objects.get(pk=id).spendings.all()
    sum = 0
    for x in spendings:
        sum += x.amount
    update.callback_query.message.reply_text('Сумма: ' + str(sum))