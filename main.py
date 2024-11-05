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
from handlers.statistics import statistics_handler
from handlers.guides import guides_handler
from handlers.builds import builds_handler
from handlers.news import news_handler
from handlers.events import events_handler
from handlers.quizzes import quizzes_handler
from handlers.achievements import achievements_handler
from handlers.community import community_handler
from handlers.polls import polls_handler
from handlers.profile import profile_handler
from handlers.help import help_handler

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

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
            # Нові стани для нових пунктів меню
            States.STATISTICS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, statistics_handler)
            ],
            States.GUIDES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, guides_handler)
            ],
            States.BUILDS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, builds_handler)
            ],
            States.NEWS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, news_handler)
            ],
            States.EVENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, events_handler)
            ],
            States.QUIZZES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, quizzes_handler)
            ],
            States.ACHIEVEMENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, achievements_handler)
            ],
            States.COMMUNITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, community_handler)
            ],
            States.POLLS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, polls_handler)
            ],
            States.PROFILE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, profile_handler)
            ],
            States.HELP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, help_handler)
            ],
            # Додайте інші стани за потреби
        },
        fallbacks=[
            CommandHandler('start', start),
            # Додайте обробник для невідомих команд, якщо необхідно
        ]
    )
    application.add_handler(conv_handler)

    logger.info("🔄 Бот запущено.")
    application.run_polling()

if __name__ == '__main__':
    main()
