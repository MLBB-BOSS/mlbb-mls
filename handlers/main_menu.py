from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.characters import get_hero_classes_keyboard
from handlers.profile import profile_handler
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
        reply_markup = get_hero_classes_keyboard(context)
        await update.message.reply_text("Будь ласка, оберіть клас героя:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS
    elif user_input == "Профіль":
        await profile_handler(update, context)
        return States.PROFILE_MENU
    else:
        await update.message.reply_text("Ця функція наразі недоступна. Оберіть іншу опцію.")
        return States.MAIN_MENU
