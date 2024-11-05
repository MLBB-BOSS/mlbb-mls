# main.py
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)
from config.settings import TELEGRAM_BOT_TOKEN
from handlers.states import States
from handlers.start_handler import start
from handlers.main_menu import main_menu_handler
from handlers.characters import (
    handle_characters_menu,
    handle_selecting_hero_class,
    handle_selecting_hero,
    handle_hero_functions_menu,
    handle_comparison_first_hero,
    handle_comparison_second_hero,
    handle_selecting_counter_hero
)
from handlers.guides import handle_guides_menu
from handlers.tournaments import handle_tournaments_menu
from handlers.updates import handle_updates_menu
from handlers.beginner import handle_beginner_menu
from handlers.news import handle_news_menu
from handlers.help_menu import handle_help_menu
from handlers.quizzes import (
    handle_quizzes_menu,
    handle_guess_the_hero
)
from handlers.search import (
    handle_search_menu,
    handle_search_performing,
    handle_search_hero_guides
)
from handlers.comparisons import handle_comparisons_menu
from handlers.emblems import handle_emblems_menu
from handlers.items import handle_items_menu
from handlers.recommendations import handle_recommendations
from handlers.trigger_handler import trigger_handler

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Змінив рівень логування на INFO для зменшення кількості повідомлень
)
logger = logging.getLogger(__name__)

# Основна функція запуску бота
def main():
    # Ініціалізація застосунку
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Ініціалізація bot_data
    application.bot_data['last_message_time'] = {}

    # Додаємо ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            States.CHARACTERS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_characters_menu)],
            States.SELECTING_HERO_CLASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero_class)
            ],
            States.SELECTING_HERO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero)
            ],
            States.HERO_FUNCTIONS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hero_functions_menu)],
            States.COMPARISON_FIRST_HERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comparison_first_hero)],
            States.COMPARISON_SECOND_HERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comparison_second_hero)],
            States.SELECTING_COUNTER_HERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_counter_hero)],
            States.GUIDES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guides_menu)],
            States.TOURNAMENTS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tournaments_menu)],
            States.UPDATES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_updates_menu)],
            States.BEGINNER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_beginner_menu)],
            States.NEWS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_news_menu)],
            States.HELP_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_help_menu)],
            States.QUIZZES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quizzes_menu)],
            States.SEARCH_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_menu)],
            # Додайте інші стани за потребою
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, trigger_handler)
        ]
    )
    application.add_handler(conv_handler)

    # Запуск бота
    logger.info("🔄 Бот запущено.")
    application.run_polling()

if __name__ == '__main__':
    main()
