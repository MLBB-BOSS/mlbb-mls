# handlers/quizzes.py

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from handlers.start_handler import start

logger = logging.getLogger(__name__)

async def quizzes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = context.application.loop.time()
    context.bot_data.setdefault('last_message_time', {})[user_id] = current_time
    logger.debug(f"Вибір у Вікторинах: {user_input}")

    if user_input == "🎲 Почати вікторину":
        await start_quiz(update, context)
        return States.QUIZ_IN_PROGRESS
    elif user_input == "📊 Мій рейтинг":
        await show_user_rating(update, context)
        return States.QUIZZES
    elif user_input == "🧩 Вгадай героя":
        await handle_guess_the_hero(update, context)
        return States.QUIZ_IN_PROGRESS
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.QUIZZES

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = (
        "❓ **Питання:** Який герой має найбільше HP?\n\n"
        "1️⃣ Джонсон\n"
        "2️⃣ Фріджон\n"
        "3️⃣ Мінотавр\n"
        "4️⃣ Грок"
    )
    await update.message.reply_text(question, parse_mode='Markdown')
    context.user_data['quiz'] = {'question_number': 1, 'correct_answer': '4'}
    return States.QUIZ_IN_PROGRESS

async def show_user_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    rating = context.user_data.get('quiz_score', 0)
    await update.message.reply_text(f"📊 Ваш рейтинг: {rating} балів.")

async def handle_guess_the_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Функція 'Вгадай героя' ще не реалізована.")
