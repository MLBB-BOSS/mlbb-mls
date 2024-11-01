# handlers/emblems.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_emblems_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Емблемах: {user_input}")

    if user_input == "💠 Список емблем":
        await send_emblem_list(update, context)
        return States.EMBLEMS_MENU
    elif user_input == "📖 Гайд по емблемах":
        await send_emblem_guide(update, context)
        return States.EMBLEMS_MENU
    elif user_input == "🔙 Назад":
        from handlers.guides import handle_guides_menu
        await handle_guides_menu(update, context)
        return States.GUIDES_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.EMBLEMS_MENU

async def send_emblem_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    emblems = (
        "💠 **Список емблем:**\n\n"
        "- Емблема Мага\n"
        "- Емблема Асасина\n"
        "- Емблема Танка\n\n"
        "🔗 Детальніше: https://example.com/emblems"
    )
    await update.message.reply_text(emblems, parse_mode='Markdown', disable_web_page_preview=True)

async def send_emblem_guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    guide = (
        "📖 **Гайд по емблемах:**\n\n"
        "Емблеми надають додаткові бонуси вашому герою...\n\n"
        "🔗 Детальніше: https://example.com/emblem-guide"
    )
    await update.message.reply_text(guide, parse_mode='Markdown', disable_web_page_preview=True)
