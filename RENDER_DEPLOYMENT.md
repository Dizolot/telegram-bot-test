# Деплой Telegram бота на Render

Этот документ содержит пошаговые инструкции по настройке автоматического деплоя Telegram бота на платформе Render.

## Шаги для настройки

### 1. Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com) и войдите в свой аккаунт
2. Нажмите на кнопку "New" для создания нового репозитория
3. Назовите репозиторий `telegram-bot-test`
4. Выберите опцию "Public" или "Private" в зависимости от ваших предпочтений
5. Нажмите "Create repository"
6. Загрузите код бота в созданный репозиторий:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ваш-аккаунт/telegram-bot-test.git
git push -u origin main
```

### 2. Регистрация на Render

1. Перейдите на [Render](https://render.com) и зарегистрируйтесь или войдите в существующий аккаунт
2. Подтвердите свой email, если это необходимо

### 3. Создание Web Service на Render

1. В панели управления Render нажмите "New" и выберите "Web Service"
2. Подключите свой GitHub аккаунт, если это еще не сделано
3. Найдите и выберите репозиторий `telegram-bot-test`
4. Настройте сервис:
   - **Name**: `telegram-bot-test` (или любое другое имя)
   - **Region**: Выберите ближайший к вам регион
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. В разделе "Environment Variables" добавьте:
   - `TELEGRAM_BOT_TOKEN`: ваш токен Telegram бота
   - `ADMIN_CHAT_ID`: ID вашего чата в Telegram
6. Нажмите "Create Web Service"

### 4. Получение ID сервиса и API ключа Render

1. **ID сервиса**: После создания сервиса, его ID можно найти в URL страницы сервиса. Например, в URL `https://dashboard.render.com/web/srv-abc123`, ID сервиса - `srv-abc123`.

2. **API ключ**:
   - Перейдите в настройки аккаунта Render (иконка профиля -> Account Settings)
   - Выберите вкладку "API Keys"
   - Нажмите "Create API Key", дайте ему название и скопируйте сгенерированный ключ

### 5. Добавление секретов в GitHub репозиторий

1. Перейдите в настройки вашего GitHub репозитория (вкладка "Settings")
2. В боковом меню выберите "Secrets and variables" -> "Actions"
3. Нажмите "New repository secret" и добавьте следующие секреты:
   - `RENDER_API_KEY`: ваш API ключ Render
   - `RENDER_SERVICE_ID`: ID вашего сервиса на Render

## Автоматический деплой

После настройки, каждый push в ветку `main` будет автоматически запускать деплой на Render. Вы можете отслеживать статус деплоя в панели управления Render.

## Проверка работоспособности

После успешного деплоя, ваш бот должен автоматически запуститься и отправить сообщение в указанный ADMIN_CHAT_ID. Вы также можете проверить работу бота, отправив ему команду `/start` в Telegram. 