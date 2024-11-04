# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import asyncio
import logging

logger = logging.getLogger(__name__)

def get_characters_menu_keyboard():
    buttons = [
        [KeyboardButton("⚔️ Порівняння героїв"), KeyboardButton("🎯 Контргерої")],
        [KeyboardButton("🗂 Список героїв")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_guides_menu_keyboard():
    buttons = [
        [KeyboardButton("📝 Гайд 1"), KeyboardButton("📝 Гайд 2")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    user_input = update.message.text.strip()
    logger.debug(f"Вибір з головного меню: {user_input}")

    # Логіка обробки вибору меню
    if user_input == "🦸 Герої":
        # Переходимо до підменю Героїв
        reply_markup = get_characters_menu_keyboard()
        await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
        return States.CHARACTERS_MENU

    elif user_input == "📚 Гайди":
        # Переходимо до підменю Гайдів
        reply_markup = get_guides_menu_keyboard()
        await update.message.reply_text("📚 Оберіть гайд:", reply_markup=reply_markup)
        return States.GUIDES_MENU

    elif user_input == "🏆 Турніри":
        # Переходимо до підменю Турнірів
        await update.message.reply_text("🏆 Функція 'Турніри' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "🔄 Оновлення":
        # Переходимо до підменю Оновлень
        await update.message.reply_text("🔄 Функція 'Оновлення' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "🆓 Початківець":
        # Переходимо до підменю Початківця
        await update.message.reply_text("🆓 Функція 'Початківець' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "🔍 Пошук":
        # Переходимо до підменю Пошуку
        await update.message.reply_text("🔍 Функція 'Пошук' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "📰 Новини":
        # Переходимо до підменю Новин
        await update.message.reply_text("📰 Функція 'Новини' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "💡 Допомога":
        # Переходимо до підменю Допомоги
        await update.message.reply_text("💡 Функція 'Допомога' ще не реалізована.")
        return States.MAIN_MENU

    elif user_input == "🎮 Вікторини":
        # Переходимо до підменю Вікторин
        await update.message.reply_text("🎮 Функція 'Вікторини' ще не реалізована.")
        return States.MAIN_MENU

    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.MAIN_MENU
