import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)

# Получаем токен и URL из переменных окружения
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
WEBHOOK_PATH = "/webhook"  # Статичный путь — безопаснее

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация Telegram Application
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот по аренде 😊")

# Регистрируем обработчик команды
application.add_handler(CommandHandler("start", start))

# Обработка входящих webhook-запросов от Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Устанавливаем webhook и запускаем Flask-сервер
if __name__ == "__main__":
    async def setup_webhook():
        await application.bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)

    asyncio.run(setup_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
