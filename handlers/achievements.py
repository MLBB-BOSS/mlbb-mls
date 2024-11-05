# handlers/achievements.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def achievements_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    logger.info(f"User selected in Achievements: {user_input}")

    if user_input == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    else:
        # Тут можна додати логіку для відображення досягнень
        await update.message.reply_text("🏆 Функція 'Досягнення' ще не реалізована.")
        return States.ACHIEVEMENTS
