# handlers/items.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_items_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Предметах: {user_input}")

    if user_input == "🛡️ Захисні предмети":
        await send_defensive_items(update, context)
        return States.ITEMS_MENU
    elif user_input == "⚔️ Атакуючі предмети":
        await send_offensive_items(update, context)
        return States.ITEMS_MENU
    elif user_input == "🔙 Назад":
        from handlers.guides import handle_guides_menu
        await handle_guides_menu(update, context)
        return States.GUIDES_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.ITEMS_MENU

async def send_defensive_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = (
        "🛡️ **Захисні предмети:**\n\n"
        "- Предмет 1: Опис...\n"
        "- Предмет 2: Опис...\n\n"
        "🔗 Детальніше: https://example.com/defensive-items"
    )
    await update.message.reply_text(items, parse_mode='Markdown', disable_web_page_preview=True)

async def send_offensive_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = (
        "⚔️ **Атакуючі предмети:**\n\n"
        "- Предмет 1: Опис...\n"
        "- Предмет 2: Опис...\n\n"
        "🔗 Детальніше: https://example.com/offensive-items"
    )
    await update.message.reply_text(items, parse_mode='Markdown', disable_web_page_preview=True)
