import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен и webhook URL из переменных окружения
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
WEBHOOK_PATH = f"/webhook/{TOKEN}"

# Flask-приложение
app = Flask(__name__)

# Telegram-приложение
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот по аренде жилья 😊")

application.add_handler(CommandHandler("start", start))

# Flask route для webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

# Установка webhook и запуск Flask-сервера
if __name__ == "__main__":
    import asyncio

    async def setup():
        await application.bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)

    asyncio.run(setup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
