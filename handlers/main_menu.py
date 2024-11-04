# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.characters import handle_characters_menu
from handlers.guides import handle_guides_menu
from handlers.tournaments import handle_tournaments_menu
from handlers.updates import handle_updates_menu
from handlers.beginner import handle_beginner_menu
from handlers.news import handle_news_menu
from handlers.help_menu import handle_help_menu
from handlers.quizzes import handle_quizzes_menu
from handlers.search import handle_search_menu
import asyncio
import logging

logger = logging.getLogger(__name__)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    user_input = update.message.text.strip()
    logger.debug(f"Вибір з головного меню: {user_input}")

    # Логіка обробки вибору меню
    if user_input == "🦸 Герої":
        # Переходимо до меню Героїв
        return await handle_characters_menu(update, context)

    elif user_input == "📚 Гайди":
        # Переходимо до меню Гайдів
        return await handle_guides_menu(update, context)

    elif user_input == "🏆 Турніри":
        # Переходимо до меню Турнірів
        return await handle_tournaments_menu(update, context)

    elif user_input == "🔄 Оновлення":
        # Переходимо до меню Оновлень
        return await handle_updates_menu(update, context)

    elif user_input == "🆓 Початківець":
        # Переходимо до меню для початківців
        return await handle_beginner_menu(update, context)

    elif user_input == "🔍 Пошук":
        # Переходимо до меню Пошуку
        return await handle_search_menu(update, context)

    elif user_input == "📰 Новини":
        # Переходимо до меню Новин
        return await handle_news_menu(update, context)

    elif user_input == "💡 Допомога":
        # Переходимо до меню Допомоги
        return await handle_help_menu(update, context)

    elif user_input == "🎮 Вікторини":
        # Переходимо до меню Вікторин
        return await handle_quizzes_menu(update, context)

    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.MAIN_MENU
