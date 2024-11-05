# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_all_heroes
import logging

logger = logging.getLogger(__name__)

# Load all heroes
HEROES_BY_CLASS = load_all_heroes()

def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton("🦸 Герої"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("📖 Гайди"), KeyboardButton("🛠 Збірки")],
        [KeyboardButton("📰 Новини"), KeyboardButton("🎉 Події")],
        [KeyboardButton("📝 Вікторини"), KeyboardButton("🏆 Досягнення")],
        [KeyboardButton("🌐 Спільнота"), KeyboardButton("📊 Опитування")],
        [KeyboardButton("👤 Мій Профіль"), KeyboardButton("ℹ️ Допомога")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    if user_input == "🦸 Герої":
        # Display the keyboard with hero classes
        buttons = []
        classes = list(HEROES_BY_CLASS.keys())
        row = []
        for idx, class_name in enumerate(classes, 1):
            row.append(KeyboardButton(class_name))
            if idx % 3 == 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([KeyboardButton("🔙 Назад")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("Оберіть клас героя:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS
    elif user_input == "📊 Статистика":
        await statistics_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "📖 Гайди":
        await guides_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "🛠 Збірки":
        await builds_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "📰 Новини":
        await news_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "🎉 Події":
        await events_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "📝 Вікторини":
        await quizzes_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "🏆 Досягнення":
        await achievements_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "🌐 Спільнота":
        await community_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "📊 Опитування":
        await polls_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "👤 Мій Профіль":
        await profile_handler(update, context)
        return States.MAIN_MENU
    elif user_input == "ℹ️ Допомога":
        await help_handler(update, context)
        return States.MAIN_MENU
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.", reply_markup=reply_markup)
        return States.MAIN_MENU
