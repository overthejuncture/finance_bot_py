from cgitb import text
import logging

from bot.models import (
    User,
    Category,
    Spending
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
        allow_reentry=True,
    )

    add_spendings_handler = ConversationHandler(
        entry_points=[CommandHandler('add_spendings', add_spendings_command)],
        states= {
            0: [MessageHandler(Filters.text, save_spendings)]
        },
        fallbacks=[],
        allow_reentry=True,
    )

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(add_category_handler)
    dispatcher.add_handler(add_spendings_handler)
    dispatcher.add_handler(CommandHandler('list_categories', list_categories_command))
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
    id = update.message.from_user.id
    cat = Category(name=update.message.text, user=User.objects.get(telegram_id=id))
    cat.save()
    update.message.reply_text('Категория сохранена')
    return ConversationHandler.END

def list_categories_command(update: Update, context: CallbackContext):
    cats = Category.objects.filter(user=User.byUpdate(update))
    to_return = ''.join("{idx}. {name}".format(idx=idx+1, name=cat.name) for idx, cat in enumerate(cats))
    update.message.reply_text(to_return)

def add_spendings_command(update: Update, context: CallbackContext):
    update.message.reply_text('Введите количество в рублях')
    return 0

def save_spendings(update: Update, context: CallbackContext):
    text = update.message.text
    if not text.isnumeric():
        update.message.reply_text('Возможны только числа')
    spending = Spending(amount=text, user=User.byUpdate(update))
    spending.save()
    

    return ConversationHandler.END