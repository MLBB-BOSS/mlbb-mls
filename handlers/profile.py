# handlers/profile.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    logger.info(f"User {user_id} is viewing profile.")

    # Приклад відображення профілю
    profile_info = (
        f"👤 **Ваш Профіль:**\n\n"
        f"• Ім'я: {update.effective_user.first_name}\n"
        f"• Рейтинг: 100 балів\n"
        f"• Досягнення: 5\n"
    )
    await update.message.reply_text(profile_info, parse_mode='Markdown')
    return States.PROFILE
