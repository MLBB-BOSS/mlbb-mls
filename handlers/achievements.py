# handlers/achievements.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def achievements_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Досягненнях: {user_input}")

    if user_input == "🏆 Мої досягнення":
        await show_user_achievements(update, context)
        return States.ACHIEVEMENTS
    elif user_input == "📈 Лідери":
        await show_leaderboard(update, context)
        return States.ACHIEVEMENTS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.ACHIEVEMENTS

async def show_user_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏆 Ваші досягнення:\n\n- Перше місце у вікторині\n- Участь у 10 матчах")

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    leaderboard = (
        "📈 **Топ гравців:**\n\n"
        "1. @user1 - 1500 балів\n"
        "2. @user2 - 1450 балів\n"
        "3. @user3 - 1400 балів"
    )
    await update.message.reply_text(leaderboard, parse_mode='Markdown')
