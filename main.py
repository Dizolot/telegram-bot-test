import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, Application

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_message(bot, text):
    try:
        await bot.send_message(ADMIN_CHAT_ID, text)
        logger.info(f'Сообщение отправлено: {text}')
    except Exception as e:
        logger.error(f'Ошибка отправки сообщения: {e}')

async def post_init(application):
    """Функция, вызываемая после инициализации бота"""
    await send_message(application.bot, 'Тест пройден')
    await asyncio.sleep(2)  # Задержка 2 секунды
    await send_message(application.bot, 'Пока')

async def start(update, context):
    """Обработчик команды /start"""
    context.bot.send_message(update.effective_chat.id, 'Тест пройден')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())