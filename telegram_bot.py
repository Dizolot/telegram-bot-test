import os
import asyncio
import logging
import nest_asyncio  # для поддержки вложенных циклов (если требуется)
from dotenv import load_dotenv

nest_asyncio.apply()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not TELEGRAM_BOT_TOKEN:
    logger.error("Ошибка: TELEGRAM_BOT_TOKEN не найден в переменных окружения.")
    exit(1)


# Обработчик для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ваш тестовый бот. Рад вас видеть!"
    )
    logger.info(f"User {update.effective_user.id} started the bot.")


# Обработчик для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Список доступных команд:\n"
        "/start - Запустить бота\n"
        "/help - Получить помощь\n"
    )
    await update.message.reply_text(help_text)
    logger.info(f"User {update.effective_user.id} requested help.")


# Основная функция запуска бота
async def main():
    logger.info("Начало выполнения функции main.")
    
    # Создаем экземпляр приложения
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Базовые команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Отправляем сообщение администратору при запуске бота
    if ADMIN_CHAT_ID:
        try:
            admin_id = int(ADMIN_CHAT_ID)
            async def send_startup_message():
                await application.bot.send_message(
                    chat_id=admin_id,
                    text="🤖 Бот успешно запущен и готов к работе!"
                )
            
            # Запланировать отправку сообщения после запуска бота
            application.job_queue.run_once(
                lambda context: asyncio.create_task(send_startup_message()),
                0
            )
            logger.info(f"Запланирована отправка сообщения администратору (ID: {admin_id})")
        except ValueError:
            logger.error(f"Неверный формат ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
        except Exception as e:
            logger.error(f"Ошибка при настройке отправки сообщения администратору: {e}")

    logger.info("Бот запускается...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
