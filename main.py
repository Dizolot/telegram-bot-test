import os
import logging
import time
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение значений переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Функция для отправки сообщения администратору
def send_message_to_admin(bot: Bot, chat_id: str, message: str):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.error(f"Error sending message to admin: {str(e)}")

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет')

    # Отправляем сообщения администратору через интервал
    time.sleep(2)
    send_message_to_admin(context.bot, ADMIN_CHAT_ID, 'Привет')
    time.sleep(2)
    send_message_to_admin(context.bot, ADMIN_CHAT_ID, 'Пока')

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Добавляем обработчик команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()