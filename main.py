# main.py
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from config.settings import TELEGRAM_BOT_TOKEN
from handlers.states import States
from handlers.start_handler import start
from handlers.main_menu import main_menu_handler
from handlers.characters import (
    handle_selecting_hero_class,
    handle_selecting_hero,
    handle_hero_functions_menu
)
# Видаляємо зайві імпорти

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Ініціалізація bot_data
    application.bot_data['last_message_time'] = {}

    # Додаємо ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            States.SELECTING_HERO_CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero_class)],
            States.SELECTING_HERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero)],
            States.HERO_FUNCTIONS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hero_functions_menu)],
            # Додайте інші стани за потребою
        },
        fallbacks=[
            CommandHandler('start', start),
            # Можна додати обробник для невідомих команд
        ]
    )
    application.add_handler(conv_handler)

    # Запуск бота
    logger.info("🔄 Бот запущено.")
    application.run_polling()

if __name__ == '__main__':
    main()
