from bot.models import Category, Spending, User
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
    CallbackContext,
)

from bot_helper_py import (
    bot as utils,
    callback_query as callback_helper
)

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, add_spendings_command)],
        states= {
            0: [ConversationHandler(
                entry_points=[MessageHandler(Filters.text, get_savings_amount)],
                states={
                    0: [CallbackQueryHandler(get_savings_category)]
                },
                fallbacks=[]
            )],
        },
        fallbacks=[],
        allow_reentry=True,
    )

def add_spendings_command(update: Update, context: CallbackContext):
    update.message.reply_text('Введите количество в рублях')
    return 0

def get_savings_amount(update: Update, context: CallbackContext):
    text = update.message.text
    if not text.isnumeric():
        update.message.reply_text('Возможны только числа')
        return

    context.user_data['save'] = {'amount': text}
    text, reply_markup = utils.list_with_keyboard_and_pager(Category.objects.all())
    update.message.reply_text("Выберите категорию\n" + text, reply_markup=reply_markup)
    return 0

def get_savings_category(update: Update, context: CallbackContext):
    if callback_helper.is_pager_action(update.callback_query):
        cats = Category.objects.all()
        start, limit = utils.proccess_pager(update)
        text, reply_markup = utils.list_with_keyboard_and_pager(cats, start, limit)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        return

    id = callback_helper.get_data(update.callback_query).get('id')
    # TODO multiple cats
    update.callback_query.edit_message_reply_markup()
    context.user_data['category'] = id
    if _save_spendings(update, context):
        update.callback_query.message.reply_text('Сохранено')
    else:
        update.callback_query.message.reply_text('Ошибка')
    return ConversationHandler.END


def _save_spendings(update: Update, context: CallbackContext):
    spending = Spending()
    spending.user = User.byUpdate(update)
    spending.amount = context.user_data['save']['amount']
    spending.category = Category.objects.get(pk=context.user_data['category'])
    spending.save()
    return True