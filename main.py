import asyncio
import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from python_telegram_bot_utils import post_init, send_message

# Загрузка переменных окружения
load_dotenv()

# Инициализация логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text('Тест пройден')

async def main():
    # Создаем приложение
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    application = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота (включает initialize и start внутри)
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Запускаем главную функцию
    asyncio.run(main())