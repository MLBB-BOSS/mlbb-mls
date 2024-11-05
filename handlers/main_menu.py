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
        await update.message.reply_text("Тут буде статистика героїв та мета гри...")
        return States.STATISTICS
    elif user_input == "📖 Гайди":
        await update.message.reply_text("Доступні гайди по стратегії, використанню героїв та багато іншого...")
        return States.GUIDES
    elif user_input == "🛠 Збірки":
        await update.message.reply_text("Рекомендовані збірки предметів та емблем для героїв...")
        return States.BUILDS
    elif user_input == "📰 Новини":
        await update.message.reply_text("Останні новини та оновлення MLBB...")
        return States.NEWS
    elif user_input == "🎉 Події":
        await update.message.reply_text("Інформація про поточні та майбутні події...")
        return States.EVENTS
    elif user_input == "📝 Вікторини":
        await update.message.reply_text("Вікторини про MLBB...")
        return States.QUIZZES
    elif user_input == "🏆 Досягнення":
        await update.message.reply_text("Ваші досягнення у боті...")
        return States.ACHIEVEMENTS
    elif user_input == "🌐 Спільнота":
        await update.message.reply_text("Приєднуйтесь до спільноти MLBB...")
        return States.COMMUNITY
    elif user_input == "📊 Опитування":
        await update.message.reply_text("Поточні опитування та голосування...")
        return States.POLLS
    elif user_input == "👤 Мій Профіль":
        await update.message.reply_text("Ваш профіль гравця...")
        return States.PROFILE
    elif user_input == "ℹ️ Допомога":
        await update.message.reply_text("Інструкції по боту та допомога...")
        return States.HELP
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.", reply_markup=reply_markup)
        return States.MAIN_MENU
