import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, Updater

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет')

def send_message(bot, text):
    try:
        bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        logging.info(f'Сообщение "{text}" отправлено администратору')
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')

def send_initial_messages(bot):
    send_message(bot, 'Привет')
    send_message(bot, 'Пока')

def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    send_initial_messages(updater.bot)

    updater.idle()

if __name__ == '__main__':
    main()