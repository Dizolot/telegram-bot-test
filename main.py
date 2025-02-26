import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f"Привет, {user.first_name}!")

# Функция для отправки сообщений
def send_messages(context: CallbackContext) -> None:
    context.bot.send_message(context.job.context, text="Пока")

def main() -> None:
    # Инициализация бота
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    # Добавление обработчика команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Добавление задачи на отправку двух сообщений с интервалом в 2 секунды
    job_queue = updater.job_queue
    job_queue.run_once(lambda context: context.bot.send_message(context.job.context, text="Привет"), 0)
    job_queue.run_once(send_messages, 2, context=update.message.chat_id)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()