import asyncio
from telegram import Bot

async def post_init(application):
    """Функция, вызываемая после инициализации бота"""
    bot = application.bot
    await send_message(bot, 'Тест пройден', application.admin_chat_id)
    await asyncio.sleep(2)  # Задержка 2 секунды
    await send_message(bot, 'Пока', application.admin_chat_id)

async def send_message(bot, message, chat_id):
    """Отправка сообщения с логированием"""
    try:
        await bot.send_message(chat_id, message)
        print(f"Сообщение '{message}' успешно отправлено администратору")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")