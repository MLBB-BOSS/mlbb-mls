# handlers/start_handler.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton("🦸 Герої")],
        # Додайте інші кнопки за потребою
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text("👋 Вітаю! Оберіть опцію з меню:", reply_markup=reply_markup)
    return States.MAIN_MENU
