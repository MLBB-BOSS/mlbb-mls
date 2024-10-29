# bot.py

import asyncio
from telegram.ext import ApplicationBuilder
from config.settings import TELEGRAM_BOT_TOKEN
from handlers.start_handler import start_handler

async def main():
    # Перевіряємо, чи є токен для бота
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Не встановлено TELEGRAM_BOT_TOKEN в змінних оточення.")
        return

    # Створюємо бота
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додаємо обробник для команди /start
    application.add_handler(start_handler)

    # Запускаємо бота в режимі опитування
    await application.run_polling()

# Запускаємо бота
if __name__ == "__main__":
    asyncio.run(main())
