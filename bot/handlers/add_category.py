from bot.models import (
    User,
    Category
)
from bot_helper_py import bot as utils

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
        entry_points=[CommandHandler(name, add_category_command)],
        states={
            0: [MessageHandler(Filters.text, add_category)]
        },
        fallbacks=[],
        allow_reentry=True,
        run_async=True
    )

def add_category_command(update: Update, context: CallbackContext):
    utils.check(update)
    update.message.reply_text('Введите название категории')
    return 0

def add_category(update: Update, context: CallbackContext):
    id = update.message.from_user.id
    cat = Category(name=update.message.text, user=User.objects.get(telegram_id=id))
    cat.save()
    update.message.reply_text('Категория сохранена')
    return ConversationHandler.END