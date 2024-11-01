# handlers/recommendations.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
from utils.recommendations_engine import get_recommendations
import logging

logger = logging.getLogger(__name__)

async def handle_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Отримуємо клас героя від користувача
    hero_class = update.message.text.strip()
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Отримано клас героя для рекомендацій: {hero_class}")

    recommendations = get_recommendations(hero_class)
    await update.message.reply_text(recommendations)
    return States.GUIDES_MENU
