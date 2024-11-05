# handlers/community.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def community_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Спільноті: {user_input}")

    if user_input == "🌐 Форум":
        await send_forum_link(update, context)
        return States.COMMUNITY
    elif user_input == "💬 Чат":
        await send_chat_link(update, context)
        return States.COMMUNITY
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.COMMUNITY

async def send_forum_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌐 Форум MLBB спільноти:\nhttps://example.com/forum")

async def send_chat_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("💬 Чат MLBB спільноти:\nhttps://t.me/MLBB_Community")
