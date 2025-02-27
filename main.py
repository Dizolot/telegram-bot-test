import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))

async def post_init(application):
    """Функция, вызываемая после инициализации бота"""
    await send_message(application.bot, 'Привет')
    await asyncio.sleep(2)  # Задержка 2 секунды
    await send_message(application.bot, 'Пока')

async def send_message(bot: Bot, text: str):
    try:
        await bot.send_message(ADMIN_CHAT_ID, text)
        print(f'Сообщение "{text}" успешно отправлено администратору.')
    except TelegramError as e:
        print(f'Ошибка при отправке сообщения: {e}')

async def start(update, context):
    update.message.reply_text('Тест пройден')

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())