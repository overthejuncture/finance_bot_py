import logging

from bot.models import (
    User
)

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def startbot() -> None:
    updater = Updater("5550070979:AAGN4lS3kXhtY9eWN-c5eNLKa6yI3TQ0stU")
    dispatcher = updater.dispatcher

    add_category_handler = ConversationHandler(
        entry_points=[CommandHandler('add_category', add_category_command)],
        states={
            0: [MessageHandler(Filters.text, add_category)]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(add_category_handler)

    updater.start_polling()
    updater.idle()

def start_command(update: Update, context: CallbackContext):
    id = update.message.from_user.id
    user = User(telegram_id = id)
    user.save()
    update.message.reply_text('Пользователь добавлен')
    pass

def add_category_command(update: Update, context: CallbackContext):
    update.message.reply_text('Введите название категории')
    return 0

def add_category(update: Update, context: CallbackContext):
    update.message.reply_text('add category')
    return ConversationHandler.END