import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)
logger = logging.getLogger(__name__)

# Добавляем вывод логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

load_dotenv()

# Поддержка обоих вариантов имени переменной для токена
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('TELEGRAM_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
PORT = int(os.getenv('PORT', '8443'))
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # URL для вебхуков на Render

if not TELEGRAM_BOT_TOKEN:
    logger.error("Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_TOKEN не найден в переменных окружения.")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я простой бот для тестирования. Тест пройден успешно!')
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
            await send_message(application.bot, admin_id, 'Бот запущен и готов к работе!')
            await asyncio.sleep(2)  # Задержка 2 секунды
            await send_message(application.bot, admin_id, 'Используйте команду /start для начала работы.')
        except ValueError:
            logger.error(f"Неверный формат ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения администратору: {e}")

async def main():
    logger.info("Начало запуска бота...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    
    logger.info("Бот готов к запуску...")
    
    # Проверяем, запускаемся ли мы на Render (через переменную PORT)
    if 'RENDER_EXTERNAL_URL' in os.environ or WEBHOOK_URL:
        webhook_url = WEBHOOK_URL or f"https://{os.environ.get('RENDER_EXTERNAL_URL')}/{TELEGRAM_BOT_TOKEN}"
        logger.info(f"Запуск бота в режиме webhook на Render с URL: {webhook_url}")
        
        # Запуск в режиме webhook для Render
        await application.bot.set_webhook(url=webhook_url)
        await application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_BOT_TOKEN,
            webhook_url=webhook_url
        )
    else:
        # Обычный запуск через polling для локальной разработки
        logger.info("Запуск бота в режиме polling для локальной разработки...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    logger.info("Бот остановлен.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        logger.exception("Детали ошибки:")