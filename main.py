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
from handlers.main_menu import main_menu_handler
from handlers.characters import (
    handle_selecting_hero_class,
    handle_selecting_hero,
    handle_hero_functions_menu
)
from handlers.profile import profile_handler, profile_menu_handler
from handlers.start_handler import start  # Переконайтеся, що цей файл існує

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Будь ласка, встановіть TELEGRAM_BOT_TOKEN як змінну середовища.")
        return

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додаємо обробник команди /start
    application.add_handler(CommandHandler('start', start))

    # Додаємо обробник розмови
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
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

    logger.info("🔄 Бот запущено.")
    application.run_polling()

if __name__ == '__main__':
    main()
    
