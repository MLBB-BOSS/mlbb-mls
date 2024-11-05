# handlers/start_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from handlers.main_menu import get_main_menu_keyboard
from handlers.states import States

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text("Вітаємо! Оберіть опцію з меню:", reply_markup=reply_markup)
    return States.MAIN_MENU
