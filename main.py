# main.py
import logging
import asyncio  # Додано для використання asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)
from config.settings import TELEGRAM_BOT_TOKEN
from handlers import States
from handlers.start_handler import start
from handlers.main_menu import main_menu_handler
from handlers.characters import handle_characters_menu
from handlers.guides import handle_guides_menu
from handlers.tournaments import handle_tournaments_menu
from handlers.updates import handle_updates_menu
from handlers.beginner import handle_beginner_menu
from handlers.news import handle_news_menu
from handlers.help_menu import handle_help_menu
from handlers.quizzes import handle_quizzes_menu
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

# Визначення get_chat_id, якщо він ще не визначений
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Ваш Chat ID: {chat_id}")

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Змінено на DEBUG для детального логування
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
            States.GUIDES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guides_menu)],
            States.TOURNAMENTS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tournaments_menu)],
            States.UPDATES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_updates_menu)],
            States.BEGINNER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_beginner_menu)],
            States.NEWS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_news_menu)],
            States.HELP_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_help_menu)],
            States.QUIZZES_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quizzes_menu)],
            States.SEARCH_PERFORMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_performing)],
            States.SEARCH_HERO_GUIDES: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_hero_guides)],
            States.COMPARISONS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comparisons_menu)],
            States.EMBLEMS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_emblems_menu)],
            States.ITEMS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_items_menu)],
            States.RECOMMENDATIONS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_recommendations)],
            # Додайте інші стани та обробники за потребою
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, trigger_handler)
        ]
    )
    application.add_handler(conv_handler)

    # Додаємо обробник для команди /get_chat_id
    application.add_handler(CommandHandler("get_chat_id", get_chat_id))

    # Додаємо обробник помилок
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error(msg="Виникла помилка:", exc_info=context.error)
    application.add_error_handler(error_handler)

    logger.info("🔄 Бот запущено.")
    application.run_polling()

# Запуск бота
if __name__ == '__main__':
    main()
    
