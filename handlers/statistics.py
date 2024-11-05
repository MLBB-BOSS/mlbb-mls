# handlers/statistics.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States

async def statistics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Тут ви можете реалізувати логіку для відображення статистики
    await update.message.reply_text("Тут буде статистика героїв та мета гри...")
    # Повертаємося до головного меню після виконання
    return States.MAIN_MENU
