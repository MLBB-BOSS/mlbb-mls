# handlers/tournaments.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_tournaments_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Турнірах: {user_input}")
    
    if user_input == "📅 Розклад турнірів":
        await send_tournament_schedule(update, context)
        return States.TOURNAMENTS_MENU
    elif user_input == "🏆 Результати турнірів":
        await send_tournament_results(update, context)
        return States.TOURNAMENTS_MENU
    elif user_input == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.TOURNAMENTS_MENU

async def send_tournament_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    schedule = "📅 **Розклад майбутніх турнірів:**\n\n" \
               "• Турнір 1 - 10 листопада\n" \
               "• Турнір 2 - 20 листопада\n\n" \
               "🔗 Детальніше: https://example.com/tournaments"
    await update.message.reply_text(schedule, parse_mode='Markdown', disable_web_page_preview=True)

async def send_tournament_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    results = "🏆 **Останні результати турнірів:**\n\n" \
              "• Турнір 1 - Переможець: Команда А\n" \
              "• Турнір 2 - Переможець: Команда Б\n\n" \
              "🔗 Детальніше: https://example.com/results"
    await update.message.reply_text(results, parse_mode='Markdown', disable_web_page_preview=True)
