import os
import asyncio
from dotenv import load_dotenv
from python_telegram_bot import Application, CommandHandler, Update, send_message

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

async def start(update, context):
    await send_message(context.bot, update.message.chat_id, 'Тест пройден')

async def post_init(application):
    await send_message(application.bot, ADMIN_CHAT_ID, 'Привет')
    await asyncio.sleep(2)  # Задержка 2 секунды
    await send_message(application.bot, ADMIN_CHAT_ID, 'Пока')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())