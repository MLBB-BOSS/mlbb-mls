# handlers/profile.py
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States

logger = logging.getLogger(__name__)

def get_profile_menu_keyboard():
    buttons = [
        [KeyboardButton("Статистика"), KeyboardButton("Події")],
        [KeyboardButton("Досягнення"), KeyboardButton("Опитування")],
        [KeyboardButton("Допомога"), KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = get_profile_menu_keyboard()
    await update.message.reply_text("👤 *Ваш Профіль*. Оберіть опцію:", parse_mode='Markdown', reply_markup=reply_markup)
    return States.PROFILE_MENU

async def profile_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    logger.info(f"User selected in Profile Menu: {user_input}")

    if user_input == "Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    elif user_input == "Статистика":
        await show_user_statistics(update, context)
        return States.PROFILE_MENU
    elif user_input == "Події":
        await update.message.reply_text("🎉 *Ваші події*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    elif user_input == "Досягнення":
        await update.message.reply_text("🏆 *Ваші досягнення*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    elif user_input == "Опитування":
        await update.message.reply_text("📊 *Ваші опитування*: ...", parse_mode='Markdown')
        return States.PROFILE_MENU
    elif user_input == "Допомога":
        await update.message.reply_text("ℹ️ *Допомога по профілю*: ...", parse_mode='Markdown')
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
        'last_login': 'Невідомо'
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
    
