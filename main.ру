import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загружаем токен и URL из переменных окружения
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
WEBHOOK_PATH = f"/{8120286970:AAEsXRKDux2-jE2TsHN8z2Z308I4D4FId1U}"

# Flask-приложение
app = Flask(__name__)

# Telegram Application
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Telegram-бот по аренде 😊")

# Добавляем обработчик в приложение
application.add_handler(CommandHandler("start", start))

# Приём webhook от Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Устанавливаем webhook и запускаем сервер
if __name__ == "__main__":
    import asyncio

    async def setup():
        await application.bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)

    asyncio.run(setup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
