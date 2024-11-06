# main.py

import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.gpt_handler import handle_ai_query  # Імпорт функції для роботи з OpenAI
import asyncio
from telegram import Update

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник для команди /start"""
    await update.message.reply_text("Привіт! Я бот з підтримкою штучного інтелекту. Напишіть мені щось, і я відповім.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник для будь-якого текстового повідомлення від користувача"""
    user_message = update.message.text
    ai_response = await handle_ai_query(user_message)
    await update.message.reply_text(ai_response)

async def main():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    if not TELEGRAM_BOT_TOKEN:
        logger.error("Будь ласка, встановіть TELEGRAM_BOT_TOKEN як змінну середовища.")
        return

    # Ініціалізація бота
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додаємо обробник команди /start
    application.add_handler(CommandHandler('start', start))

    # Додаємо обробник для всіх текстових повідомлень
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🔄 Бот запущено.")
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
