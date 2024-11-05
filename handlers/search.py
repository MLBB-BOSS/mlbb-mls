# handlers/search.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def handle_search_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [KeyboardButton("🔍 Пошук героїв та гайдів"), KeyboardButton("🎙️ Голосовий пошук")],
        [KeyboardButton("📝 Історія пошуку"), KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
    return States.SEARCH_PERFORMING

async def handle_search_performing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()

    # Перевірка на опції головного меню
    main_menu_options = ["🦸 Герої", "📊 Статистика", "📖 Гайди", "🛠 Збірки", "📰 Новини", "🎉 Події",
                         "📝 Вікторини", "🏆 Досягнення", "🌐 Спільнота", "📊 Опитування", "👤 Мій Профіль",
                         "ℹ️ Допомога", "🔍 Пошук"]

    if user_input in main_menu_options:
        from handlers.main_menu import main_menu_handler
        await main_menu_handler(update, context)
        return States.MAIN_MENU

    if user_input == "🔙 Назад":
        from handlers.main_menu import main_menu_handler, get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    elif user_input == "🔍 Пошук героїв та гайдів":
        await update.message.reply_text("🔍 Введіть ваш запит для пошуку:")
        return States.SEARCH_HERO_GUIDES
    elif user_input == "🎙️ Голосовий пошук":
        await update.message.reply_text("🎙️ Голосовий пошук наразі не підтримується.")
        return States.SEARCH_PERFORMING
    elif user_input == "📝 Історія пошуку":
        await show_search_history(update, context)
        return States.SEARCH_PERFORMING
    else:
        query = user_input
        return await perform_search(query, update, context)
