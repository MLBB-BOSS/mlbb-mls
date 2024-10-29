# handlers/start_handler.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.main_menu import main_menu_handler
from handlers import States

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    buttons = [
        [KeyboardButton("🧙‍♂️ Персонажі"), KeyboardButton("📚 Гайди"), KeyboardButton("🏆 Турніри")],
        [KeyboardButton("🔄 Оновлення"), KeyboardButton("🆓 Початківець"), KeyboardButton("🔍 Пошук")],
        [KeyboardButton("📰 Новини"), KeyboardButton("💡 Допомога"), KeyboardButton("🎮 Вікторини")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
    return States.MAIN_MENU
