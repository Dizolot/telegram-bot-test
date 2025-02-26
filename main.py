import os
import logging
import time
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена бота из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Проверка наличия переменных окружения
if not TELEGRAM_BOT_TOKEN or not ADMIN_CHAT_ID:
    logger.error("Необходимо указать TELEGRAM_BOT_TOKEN и ADMIN_CHAT_ID в переменных окружения")
    exit(1)

# Функция для отправки сообщений
def send_message(bot: Bot, chat_id: str, text: str):
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет")

# Функция для отправки сообщений администратору
def send_initial_messages(bot: Bot):
    send_message(bot, ADMIN_CHAT_ID, "Привет")
    time.sleep(2)
    send_message(bot, ADMIN_CHAT_ID, "Пока")

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Обработка команды /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Запуск бота
    updater.start_polling()

    # Отправка сообщений администратору
    send_initial_messages(updater.bot)

    updater.idle()

if __name__ == '__main__':
    main()