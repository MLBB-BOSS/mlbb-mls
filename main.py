# Main f# main.py
import asyncio
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
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
from handlers.search import handle_search_menu
from utils.data_loader import load_json_data
# main.py (додайте в main функцію перед запуском бота)
application.bot_data['last_message_time'] = {}

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Завантаження даних
prompts_data = load_json_data('data/prompts.json')
heroes_data = load_json_data('data/characters.json')

# Основна функція запуску бота
async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_chat_id", get_chat_id))
    
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
            States.SEARCH_PERFORMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_menu)],
            # Додайте інші стани тут за потребою
        },
        fallbacks=[CommandHandler('start', start)]
    )
    application.add_handler(conv_handler)
    
    # Додаємо обробник помилок
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error(msg="Виникла помилка:", exc_info=context.error)
    application.add_error_handler(error_handler)
    
    logger.info("🔄 Бот запущено.")
    await application.run_polling()

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
ile for the bot
