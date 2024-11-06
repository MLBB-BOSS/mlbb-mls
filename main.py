# main.py

import logging
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from handlers.states import States
from handlers.main_menu import main_menu_handler, unknown_command
from handlers.profile import profile_handler, profile_menu_handler
from handlers.start_handler import start
from utils.data_loader import load_all_heroes, load_heroes_data
from utils.formatting import format_ai_response  # Імпорт функції форматування
from utils.gpt_handler import handle_gpt_query  # Імпорт функції для роботи з OpenAI
import asyncio
import random
from telegram import Update

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_trigger_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()

    TRIGGER_WORDS = ["герой", "персонаж", "геймплей", "mlbb", "mobile legends"]  # Приклад тригерних слів

    if any(trigger in message_text for trigger in TRIGGER_WORDS):
        # Вибір випадкового героя
        heroes_data = context.bot_data.get('heroes_data', {})
        if not heroes_data:
            await update.message.reply_text("⚠️ Інформація про героїв наразі недоступна.")
            return

        hero_name = random.choice(list(heroes_data.keys()))
        # Виклик функції handle_gpt_query
        gpt_response = await handle_gpt_query(hero_name, context)
        await update.message.reply_text(gpt_response, parse_mode='HTML', disable_web_page_preview=True)

async def main():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if not TELEGRAM_BOT_TOKEN:
        logger.error("Будь ласка, встановіть TELEGRAM_BOT_TOKEN як змінну середовища.")
        return

    if not OPENAI_API_KEY:
        logger.error("Будь ласка, встановіть OPENAI_API_KEY як змінну середовища.")
        return

    # Завантаження даних про героїв
    heroes_by_class = load_all_heroes()
    heroes_data = load_heroes_data()

    # Ініціалізація бота
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додаємо обробник команди /start
    application.add_handler(CommandHandler('start', start))

    # Додаємо ConversationHandler для складних сценаріїв
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)
            ],
            States.SELECTING_HERO_CLASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero_class)
            ],
            States.SELECTING_HERO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero)
            ],
            States.HERO_FUNCTIONS_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hero_functions_menu)
            ],
            States.PROFILE_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, profile_menu_handler)
            ],
            # Додайте інші стани за потреби
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(filters.COMMAND, unknown_command)  # Обробка невідомих команд
        ]
    )
    application.add_handler(conv_handler)

    # Додаємо обробник невідомих команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Додаємо обробник тригерних слів
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_trigger_words))

    # Зберігаємо завантажені дані в bot_data
    application.bot_data['heroes_by_class'] = heroes_by_class
    application.bot_data['heroes_data'] = heroes_data

    logger.info("🔄 Бот запущено.")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
