# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from handlers import States
import asyncio  # Додано для використання asyncio
import logging

logger = logging.getLogger(__name__)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()  # Отримуємо поточний час
    context.bot_data['last_message_time'][user_id] = current_time

    user_input = update.message.text.strip()
    logger.debug(f"Вибір з головного меню: {user_input}")

    # Логіка обробки вибору меню
    if user_input == "🧙‍♂️ Персонажі":
        # Перехід до підменю Персонажів
        buttons = [
            [KeyboardButton("📝 Деталі про героїв"), KeyboardButton("🧩 Вгадай героя")],
            [KeyboardButton("⚔️ Порівняння героїв"), KeyboardButton("🎯 Контргерої")],
            [KeyboardButton("🗂 Список героїв"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🧙‍♂️ Оберіть опцію:", reply_markup=reply_markup)
        return States.CHARACTERS_MENU

    elif user_input == "🔍 Пошук":
        # Перехід до пошуку
        buttons = [
            [KeyboardButton("🔍 Пошук героїв та гайдів"), KeyboardButton("🎙️ Голосовий пошук")],
            [KeyboardButton("📝 Історія пошуку"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🔍 Оберіть опцію пошуку:", reply_markup=reply_markup)
        return States.SEARCH_PERFORMING

    elif user_input == "🆓 Початківець":
        # Перехід до підменю Початківців
        buttons = [
            [KeyboardButton("👶 Початковий гайд"), KeyboardButton("📖 Базові поради")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🆓 Оберіть опцію для початківців:", reply_markup=reply_markup)
        return States.BEGINNER_MENU

    elif user_input == "📚 Гайди":
        # Перехід до підменю Гайдів
        buttons = [
            [KeyboardButton("📝 Стратегії для кожного класу"), KeyboardButton("💡 Інтерактивні рекомендації")],
            [KeyboardButton("🎥 Відео-гайди"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("📚 Оберіть опцію гайдів:", reply_markup=reply_markup)
        return States.GUIDES_MENU

    elif user_input == "🏆 Турніри":
        # Перехід до підменю Турнірів
        buttons = [
            [KeyboardButton("📅 Розклад турнірів"), KeyboardButton("🏆 Результати турнірів")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🏆 Оберіть опцію турнірів:", reply_markup=reply_markup)
        return States.TOURNAMENTS_MENU

    elif user_input == "🔄 Оновлення":
        # Перехід до підменю Оновлень
        buttons = [
            [KeyboardButton("🆕 Останні оновлення"), KeyboardButton("📄 Патчноути")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🔄 Оберіть опцію оновлень:", reply_markup=reply_markup)
        return States.UPDATES_MENU

    elif user_input == "📰 Новини":
        # Перехід до підменю Новин
        buttons = [
            [KeyboardButton("📰 Останні новини"), KeyboardButton("💬 Обговорення")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("📰 Оберіть опцію новин:", reply_markup=reply_markup)
        return States.NEWS_MENU

    elif user_input == "💡 Допомога":
        # Перехід до підменю Допомоги
        buttons = [
            [KeyboardButton("❓ FAQ"), KeyboardButton("💬 Живий чат підтримки")],
            [KeyboardButton("🐞 Повідомлення про помилки"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("💡 Оберіть опцію допомоги:", reply_markup=reply_markup)
        return States.HELP_MENU

    elif user_input == "🎮 Вікторини":
        # Перехід до підменю Вікторин
        buttons = [
            [KeyboardButton("🎲 Почати вікторину"), KeyboardButton("📊 Мій рейтинг")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🎮 Оберіть опцію вікторин:", reply_markup=reply_markup)
        return States.QUIZZES_MENU

    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.MAIN_MENU
        
