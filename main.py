import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from typing import Any, Dict

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена бота и ID администратора из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Функция, вызываемая после инициализации бота"""
    try:
        await send_message(application.bot, 'Привет')
        await asyncio.sleep(2)  # Задержка 2 секунды
        await send_message(application.bot, 'Пока')
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения: {str(e)}')

async def send_message(bot: Any, text: str) -> None:
    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        logger.info(f'Сообщение "{text}" успешно отправлено')
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения: {str(e)}')

async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    update.message.reply_text('Привет')

async def main():
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Запускаем бота (включает initialize и start внутри)
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Запускаем главную функцию
    asyncio.run(main())