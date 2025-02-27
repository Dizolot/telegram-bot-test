import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TELEGRAM_BOT_TOKEN:
    logger.error("Ошибка: TELEGRAM_BOT_TOKEN не найден в переменных окружения.")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Тест пройден')
    logger.info(f"User {update.effective_user.id} started the bot.")

async def send_message(bot, chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Сообщение '{text}' успешно отправлено в чат {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def post_init(application):
    if ADMIN_CHAT_ID:
        try:
            admin_id = int(ADMIN_CHAT_ID)
            await send_message(application.bot, admin_id, 'Привет')
            await asyncio.sleep(2)  # Задержка 2 секунды
            await send_message(application.bot, admin_id, 'Пока')
        except ValueError:
            logger.error(f"Неверный формат ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения администратору: {e}")

async def main():
    logger.info("Начало запуска бота...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    
    logger.info("Бот запускается...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")