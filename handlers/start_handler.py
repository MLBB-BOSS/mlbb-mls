# handlers/start_handler.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler
from config.settings import TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Створення кнопок меню
    buttons = [
        [KeyboardButton("🧙‍♂️ Персонажі"), KeyboardButton("📚 Гайди"), KeyboardButton("🏆 Турніри")],
        [KeyboardButton("🔄 Оновлення"), KeyboardButton("🆓 Початківець"), KeyboardButton("🔍 Пошук")],
        [KeyboardButton("📰 Новини"), KeyboardButton("💡 Допомога"), KeyboardButton("🎮 Вікторини")]
    ]
    
    # Створення клавіатури з кнопками
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # Відправка повідомлення користувачу з клавіатурою
    await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)

# Створення обробника команди /start
start_handler = CommandHandler("start", start)
