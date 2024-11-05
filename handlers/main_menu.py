# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton("🦸 Герої"), KeyboardButton("📊 Статистика"), KeyboardButton("📖 Гайди")],
        [KeyboardButton("🛠 Збірки"), KeyboardButton("📰 Новини"), KeyboardButton("🎉 Події")],
        [KeyboardButton("📝 Вікторини"), KeyboardButton("🏆 Досягнення"), KeyboardButton("🌐 Спільнота")],
        [KeyboardButton("📊 Опитування"), KeyboardButton("👤 Мій Профіль"), KeyboardButton("ℹ️ Допомога")],
        [KeyboardButton("🔍 Пошук")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    if user_input == "🦸 Герої":
        # Ваш код для обробки вибору "Герої"
        pass
    elif user_input == "🔍 Пошук":
        await update.message.reply_text("Введіть ім'я героя для пошуку:")
        return States.SEARCH_HERO
    elif user_input == "👤 Мій Профіль":
        from handlers.profile import profile_handler
        return await profile_handler(update, context)
    # Інші умови...
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.", reply_markup=reply_markup)
        return States.MAIN_MENU
