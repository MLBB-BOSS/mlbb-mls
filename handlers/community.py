# handlers/community.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def community_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    logger.info(f"User selected in Community: {user_input}")

    if user_input == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    else:
        # Тут можна додати логіку для відображення спільноти
        community_links = (
            "🌐 **Спільнота MLBB:**\n\n"
            "• [Офіційний Discord сервер](https://discord.gg/yourserver)\n"
            "• [Група в Facebook](https://facebook.com/yourgroup)\n"
            "• [Форум гравців](https://example.com/forum)"
        )
        await update.message.reply_text(community_links, parse_mode='Markdown', disable_web_page_preview=True)
        return States.COMMUNITY
