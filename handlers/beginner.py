# handlers/beginner.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_beginner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Початківцях: {user_input}")
    
    if user_input == "👶 Початковий гайд":
        await send_beginner_guide(update, context)
        return States.BEGINNER_MENU
    elif user_input == "📖 Базові поради":
        await send_basic_tips(update, context)
        return States.BEGINNER_MENU
    elif user_input == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.BEGINNER_MENU

async def send_beginner_guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    guide = (
        "👶 **Початковий гайд:**\n\n"
        "• Крок 1: Ознайомтеся з інтерфейсом.\n"
        "• Крок 2: Виберіть свого першого героя.\n"
        "• Крок 3: Пройдіть тренувальний режим.\n\n"
        "🔗 Детальніше: https://example.com/beginner-guide"
    )
    await update.message.reply_text(
        guide, parse_mode='Markdown', disable_web_page_preview=True
    )

async def send_basic_tips(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tips = (
        "📖 **Базові поради:**\n\n"
        "• Завжди слідкуйте за картою.\n"
        "• Командна робота - ключ до перемоги.\n"
        "• Вивчайте навички свого героя.\n\n"
        "🔗 Детальніше: https://example.com/basic-tips"
    )
    await update.message.reply_text(
        tips, parse_mode='Markdown', disable_web_page_preview=True
    )
