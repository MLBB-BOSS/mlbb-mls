# handlers/events.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def events_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Подіях: {user_input}")

    if user_input == "🎉 Поточні події":
        await send_current_events(update, context)
        return States.EVENTS
    elif user_input == "📅 Майбутні події":
        await send_upcoming_events(update, context)
        return States.EVENTS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.EVENTS

async def send_current_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    events = (
        "🎉 **Поточні події:**\n\n"
        "• Подія 'Зимовий фестиваль' триває до 31 грудня.\n"
        "• Турнір 'Битва за славу' розпочався!\n\n"
        "🔗 Детальніше: https://example.com/current-events"
    )
    await update.message.reply_text(events, parse_mode='Markdown', disable_web_page_preview=True)

async def send_upcoming_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    upcoming_events = (
        "📅 **Майбутні події:**\n\n"
        "• Новий сезон розпочнеться 1 січня.\n"
        "• Анонс нового героя 15 січня.\n\n"
        "🔗 Детальніше: https://example.com/upcoming-events"
    )
    await update.message.reply_text(upcoming_events, parse_mode='Markdown', disable_web_page_preview=True)
