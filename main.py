import os
import logging
from time import sleep
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()

# Настройка логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для отправки сообщения администратору
def send_message_to_admin(bot: Bot, admin_chat_id: int, text: str):
    try:
        bot.send_message(chat_id=admin_chat_id, text=text)
        logger.info(f"Message sent to admin: {text}")
    except Exception as e:
        logger.error(f"Error sending message to admin: {e}")

# Функция обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет')

def main():
    # Проверка наличия переменных окружения
    if 'TELEGRAM_BOT_TOKEN' not in os.environ or 'ADMIN_CHAT_ID' not in os.environ:
        logger.error("Missing TELEGRAM_BOT_TOKEN or ADMIN_CHAT_ID in environment variables")
        return

    # Инициализация бота
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    admin_chat_id = int(os.getenv('ADMIN_CHAT_ID'))
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Добавление обработчика команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Отправка сообщения администратору сразу после запуска
    bot = updater.bot
    send_message_to_admin(bot, admin_chat_id, 'Привет')

    # Отправка второго сообщения через 2 секунды
    sleep(2)
    send_message_to_admin(bot, admin_chat_id, 'Пока')

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()