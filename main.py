import os
import logging
from threading import Timer
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Идентификатор администратора
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Функция для отправки сообщения администратору
def send_message(bot, chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        logger.info(f'Сообщение "{text}" успешно отправлено администратору')
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения: {e}')

# Функция для автоматической отправки сообщений администратору
def send_initial_messages():
    bot = Bot(token=TOKEN)
    send_message(bot, ADMIN_CHAT_ID, 'Привет')
    Timer(2, send_message, (bot, ADMIN_CHAT_ID, 'Пока')).start()

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет')

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Запуск функции автоматической отправки сообщений администратору
    send_initial_messages()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()