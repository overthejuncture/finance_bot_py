import logging
from .handlers import (
    list_categories,
    start,
    add_category,
    add_spendings
)

from telegram.ext import (
    Updater,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def startbot() -> None:
    updater = Updater("5550070979:AAGN4lS3kXhtY9eWN-c5eNLKa6yI3TQ0stU")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start.handler('start'))
    dispatcher.add_handler(add_category.handler('add_category'))
    dispatcher.add_handler(add_spendings.handler('add_spendings'))
    dispatcher.add_handler(list_categories.handler('list_categories'))

    updater.start_polling()
    updater.idle()
