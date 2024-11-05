# handlers/news.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def news_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Новинах: {user_input}")

    if user_input == "📰 Останні новини":
        await send_latest_news(update, context)
        return States.NEWS
    elif user_input == "💬 Обговорення":
        await send_discussion_forum(update, context)
        return States.NEWS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.NEWS

async def send_latest_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    news = (
        "📰 **Останні новини:**\n\n"
        "• Новий герой з'явиться наступного місяця!\n"
        "• Оновлення балансу героїв.\n\n"
        "🔗 Детальніше: https://example.com/latest-news"
    )
    await update.message.reply_text(news, parse_mode='Markdown', disable_web_page_preview=True)

async def send_discussion_forum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    discussion = (
        "💬 **Обговорення:**\n\n"
        "Приєднуйтесь до нашого форуму для обговорення останніх подій.\n\n"
        "🔗 [Форум обговорень](https://example.com/forum)"
    )
    await update.message.reply_text(discussion, parse_mode='Markdown', disable_web_page_preview=True)
