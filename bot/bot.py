import logging
from .handlers import (
    list_categories,
    categories_actions,
    start,
    add_category,
    add_spendings,
    list_spendings_for_category,
)

from telegram.ext import (
    Updater,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# logger = logging.getLogger('django.db.backends')    
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

def startbot() -> None:
    updater = Updater("5550070979:AAGN4lS3kXhtY9eWN-c5eNLKa6yI3TQ0stU")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start.handler('start'))
    dispatcher.add_handler(add_category.handler('add_category'))
    dispatcher.add_handler(add_spendings.handler('add_spendings'))
    dispatcher.add_handler(list_categories.handler('list_categories'))
    dispatcher.add_handler(categories_actions.handler('categories_actions'))
    dispatcher.add_handler(list_spendings_for_category.handler('list_spendings_for_category'))
 
    updater.start_polling()
    updater.idle()
