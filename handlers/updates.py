# handlers/updates.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_updates_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Оновленнях: {user_input}")
    
    if user_input == "🆕 Останні оновлення":
        await send_latest_updates(update, context)
        return States.UPDATES_MENU
    elif user_input == "📄 Патчноути":
        await send_patch_notes(update, context)
        return States.UPDATES_MENU
    elif user_input == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.UPDATES_MENU

async def send_latest_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    updates = "🆕 **Останні оновлення:**\n\n" \
              "• Додано нового героя.\n" \
              "• Покращено баланс гри.\n\n" \
              "🔗 Детальніше: https://example.com/latest-updates"
    await update.message.reply_text(updates, parse_mode='Markdown', disable_web_page_preview=True)

async def send_patch_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    patch_notes = "📄 **Патчноути:**\n\n" \
                  "• Версія 1.2.3:\n" \
                  "  - Виправлено помилки.\n" \
                  "  - Оптимізовано продуктивність.\n\n" \
                  "🔗 Детальніше: https://example.com/patch-notes"
    await update.message.reply_text(patch_notes, parse_mode='Markdown', disable_web_page_preview=True)
