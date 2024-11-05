# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton("🦸 Герої"), KeyboardButton("📖 Гайди"), KeyboardButton("🛠 Збірки")],
        [KeyboardButton("📰 Новини"), KeyboardButton("📝 Вікторини"), KeyboardButton("🌐 Спільнота")],
        [KeyboardButton("Профіль"), KeyboardButton("🔍 Пошук")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    logger.info(f"User selected in Main Menu: {user_input}")

    if user_input == "🦸 Герої":
        from handlers.characters import handle_selecting_hero_class
        await handle_selecting_hero_class(update, context)
        return States.SELECTING_HERO_CLASS
    elif user_input == "📖 Гайди":
        await update.message.reply_text("📖 Гайди наразі недоступні.")
        return States.MAIN_MENU
    elif user_input == "🛠 Збірки":
        await update.message.reply_text("🛠 Збірки наразі недоступні.")
        return States.MAIN_MENU
    elif user_input == "📰 Новини":
        await update.message.reply_text("📰 Новини наразі недоступні.")
        return States.MAIN_MENU
    elif user_input == "📝 Вікторини":
        await update.message.reply_text("📝 Вікторини наразі недоступні.")
        return States.MAIN_MENU
    elif user_input == "🌐 Спільнота":
        await update.message.reply_text("🌐 Спільнота наразі недоступна.")
        return States.MAIN_MENU
    elif user_input == "Профіль":
        from handlers.profile import profile_handler
        await profile_handler(update, context)
        return States.PROFILE_MENU
    elif user_input == "🔍 Пошук":
        from handlers.search import handle_search_menu
        await handle_search_menu(update, context)
        return States.SEARCH_PERFORMING
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.", reply_markup=reply_markup)
        return States.MAIN_MENU
