# handlers/builds.py

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def builds_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.info(f"Вибір в Збірках: {user_input}")

    if user_input == "🛠 Рекомендовані збірки":
        await send_recommended_builds(update, context)
        return States.BUILDS
    elif user_input == "🔧 Налаштувати збірку":
        await customize_build(update, context)
        return States.BUILDS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.BUILDS

async def send_recommended_builds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    builds_message = (
        "🛠 **Рекомендовані збірки:**\n\n"
        "• Для Танків: [Посилання](https://example.com/tank-builds)\n"
        "• Для Магів: [Посилання](https://example.com/mage-builds)\n"
        "• Для Стрільців: [Посилання](https://example.com/marksman-builds)\n\n"
        "🔗 Детальніше: https://example.com/builds"
    )
    await update.message.reply_text(builds_message, parse_mode='Markdown', disable_web_page_preview=True)

async def customize_build(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔧 Функція налаштування збірки ще не реалізована.")
