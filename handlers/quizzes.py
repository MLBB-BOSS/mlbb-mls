# handlers/quizzes.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
import logging

logger = logging.getLogger(__name__)

async def handle_quizzes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір у Вікторинах: {user_input}")

    if user_input == "🎲 Почати вікторину":
        await start_quiz(update, context)
        return States.QUIZZES_MENU
    elif user_input == "📊 Мій рейтинг":
        await show_user_rating(update, context)
        return States.QUIZZES_MENU
    elif user_input == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.QUIZZES_MENU

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Приклад простої вікторини
    question = (
        "❓ **Питання:** Який герой має найбільше HP?\n\n"
        "1️⃣ Джонсон\n"
        "2️⃣ Фрідом\n"
        "3️⃣ Муна\n"
        "4️⃣ Анні"
    )
    await update.message.reply_text(question, parse_mode='Markdown')
    # Збереження стану вікторини
    context.user_data['quiz'] = {'question': 1}

async def show_user_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Приклад показу рейтингу
    await update.message.reply_text("📊 Ваш рейтинг: 100 балів.")
