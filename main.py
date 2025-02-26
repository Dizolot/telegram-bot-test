import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет')
    context.job_queue.run_once(send_bye, 2, context=update.message.chat_id)

def send_bye(context: CallbackContext) -> None:
    context.bot.send_message(context.job.context, text='Пока')

def main() -> None:
    # Инициализация бота
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
    dispatcher = updater.dispatcher

    # Добавление обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()