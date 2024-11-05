# handlers/profile.py

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import datetime

logger = logging.getLogger(__name__)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("📋 Опитування")],
        [KeyboardButton("ℹ️ Допомога"), KeyboardButton("🎉 Події")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("👤 *Ваш Профіль*. Оберіть опцію:", parse_mode='Markdown', reply_markup=reply_markup)
    return States.PROFILE_MENU

async def profile_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    logger.info(f"User selected in Profile Menu: {user_input}")

    # Перевірка на опції головного меню
    main_menu_options = ["🦸 Герої", "📊 Статистика", "📖 Гайди", "🛠 Збірки", "📰 Новини", "🎉 Події",
                         "📝 Вікторини", "🏆 Досягнення", "🌐 Спільнота", "📊 Опитування", "👤 Мій Профіль",
                         "ℹ️ Допомога", "🔍 Пошук"]

    if user_input in main_menu_options:
        from handlers.main_menu import main_menu_handler
        await main_menu_handler(update, context)
        return States.MAIN_MENU

    if user_input == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    elif user_input == "📊 Статистика":
        await show_user_statistics(update, context)
        return States.PROFILE_MENU
    elif user_input == "📋 Опитування":
        await update.message.reply_text("📋 *Ваші опитування*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    elif user_input == "ℹ️ Допомога":
        await update.message.reply_text("ℹ️ *Допомога по профілю*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    elif user_input == "🎉 Події":
        await update.message.reply_text("🎉 *Ваші події*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.PROFILE_MENU
