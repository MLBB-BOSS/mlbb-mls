# handlers/profile.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Мій Профіль: {user_input}")

    if user_input == "👤 Мій профіль":
        await show_user_profile(update, context)
        return States.PROFILE
    elif user_input == "⚙️ Налаштування":
        await profile_settings(update, context)
        return States.PROFILE
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.PROFILE

async def show_user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"👤 Ваш профіль:\n\nІм'я: {user.first_name}\nID: {user.id}")

async def profile_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⚙️ Функція налаштувань профілю ще не реалізована.")
