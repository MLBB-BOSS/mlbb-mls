# handlers/quizzes.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import asyncio
import logging

logger = logging.getLogger(__name__)

async def handle_quizzes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time
    logger.debug(f"Вибір у Вікторинах: {user_input}")

    if user_input == "🎲 Почати вікторину":
        await start_quiz(update, context)
        return States.QUIZZES_MENU
    elif user_input == "📊 Мій рейтинг":
        await show_user_rating(update, context)
        return States.QUIZZES_MENU
    elif user_input == "🧩 Вгадай героя":
        await handle_guess_the_hero(update, context)
        return States.QUIZZES_MENU
    elif user_input == "🔙 Назад":
        from handlers.start_handler import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
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

async def handle_guess_the_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Реалізація функції "Вгадай героя"
    await update.message.reply_text("Функція 'Вгадай героя' ще не реалізована.")
