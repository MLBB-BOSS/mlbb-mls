# handlers/start_handler.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import asyncio
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    buttons = [
        [KeyboardButton("🧙‍♂️ Персонажі"), KeyboardButton("📚 Гайди"), KeyboardButton("🏆 Турніри")],
        [KeyboardButton("🔄 Оновлення"), KeyboardButton("🆓 Початківець"), KeyboardButton("🔍 Пошук")],
        [KeyboardButton("📰 Новини"), KeyboardButton("💡 Допомога"), KeyboardButton("🎮 Вікторини")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("👋 Вітаю! Оберіть опцію з меню:", reply_markup=reply_markup)
    return States.MAIN_MENU
