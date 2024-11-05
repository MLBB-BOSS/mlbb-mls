# handlers/polls.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def polls_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Опитуваннях: {user_input}")

    if user_input == "📊 Поточні опитування":
        await send_current_polls(update, context)
        return States.POLLS
    elif user_input == "🗳 Голосувати":
        await vote_in_poll(update, context)
        return States.POLLS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.POLLS

async def send_current_polls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    polls = (
        "📊 **Поточні опитування:**\n\n"
        "1️⃣ Який ваш улюблений клас героїв?\n"
        "2️⃣ Яка ваша улюблена карта?\n\n"
        "🔗 Виберіть '🗳 Голосувати', щоб взяти участь."
    )
    await update.message.reply_text(polls, parse_mode='Markdown')

async def vote_in_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🗳 Функція голосування ще не реалізована.")
