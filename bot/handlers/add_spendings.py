from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    CallbackContext,
)

def handler(name: str):
    return ConversationHandler(
        entry_points=[CommandHandler(name, add_spendings_command)],
        states= {
            0: [MessageHandler(Filters.text, get_savings_amount)],
            1: [MessageHandler(Filters.text, get_savings_category)],
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
        return 0

    context.user_data['save']['amount'] = text
    update.message.reply_text('Выберите категорию')
    return 1

def get_savings_category(update: Update, context: CallbackContext):
    pass
    # spending = Spending(amount=context.user_data['save']['amount'], user=User.byUpdate(update))
    # spending.save()