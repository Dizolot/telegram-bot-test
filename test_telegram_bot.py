import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

# Импортируем функции из нашего бота
from telegram_bot import start, help_command

# Загружаем переменные окружения
load_dotenv()

# Фикстура для создания мока объекта Update
@pytest.fixture
def update():
    update = AsyncMock(spec=Update)
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()
    return update

# Фикстура для создания мока объекта Context
@pytest.fixture
def context():
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    return context

# Тест для команды /start
@pytest.mark.asyncio
async def test_start_command(update, context):
    # Вызываем функцию start
    await start(update, context)
    
    # Проверяем, что был вызван метод reply_text с правильным сообщением
    update.message.reply_text.assert_called_once_with(
        "Привет! Я ваш тестовый бот. Рад вас видеть!"
    )

# Тест для команды /help
@pytest.mark.asyncio
async def test_help_command(update, context):
    # Вызываем функцию help_command
    await help_command(update, context)
    
    # Проверяем, что был вызван метод reply_text с правильным сообщением
    help_text = (
        "Список доступных команд:\n"
        "/start - Запустить бота\n"
        "/help - Получить помощь\n"
    )
    update.message.reply_text.assert_called_once_with(help_text)

# Запуск тестов
if __name__ == "__main__":
    pytest.main(["-xvs", "test_telegram_bot.py"]) 