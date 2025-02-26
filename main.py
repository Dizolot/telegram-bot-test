import os
import logging
from time import sleep
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Функция для отправки сообщений администратору
def send_message(bot, chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Message sent to {chat_id}: {text}")
    except Exception as e:
        logger.error(f"Error sending message to {chat_id}: {e}")

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет')

def main():
    if not TOKEN or not ADMIN_CHAT_ID:
        logger.error("Please provide TELEGRAM_BOT_TOKEN and ADMIN_CHAT_ID in environment variables.")
        return

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    bot = Bot(token=TOKEN)
    
    send_message(bot, ADMIN_CHAT_ID, 'Привет')
    sleep(2)
    send_message(bot, ADMIN_CHAT_ID, 'Пока')

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()