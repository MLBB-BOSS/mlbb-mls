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

async def show_user_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    stats = context.user_data.get('statistics', {
        'games_played': 0,
        'heroes_unlocked': 0,
        'achievements': 0,
        'last_login': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    stats_text = (
        f"📊 *Ваша статистика:*\n\n"
        f"👤 Ім'я: {user.first_name}\n"
        f"🎮 Ігор зіграно: {stats['games_played']}\n"
        f"🦸 Героїв розблоковано: {stats['heroes_unlocked']}\n"
        f"🏆 Досягнень отримано: {stats['achievements']}\n"
        f"⏰ Останній вхід: {stats['last_login']}"
    )
    await update.message.reply_text(stats_text, parse_mode='Markdown')
