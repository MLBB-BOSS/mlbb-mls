# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    user_input = update.message.text
    logger = context.application.job_queue.logger
    logger.info(f"Вибір з головного меню: {user_input}")
    
    # Логіка обробки вибору меню
    if user_input == "🧙‍♂️ Персонажі":
        # Перехід до підменю Персонажів
        buttons = [
            [KeyboardButton("📝 Деталі про героїв"), KeyboardButton("🧩 Вгадай героя")],
            [KeyboardButton("⚔️ Порівняння героїв"), KeyboardButton("🎯 Контргерої")],
            [KeyboardButton("🗂 Список героїв"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("🧙‍♂️ Оберіть опцію:", reply_markup=reply_markup)
        return States.CHARACTERS_MENU
    elif user_input == "🔍 Пошук":
        # Перехід до пошуку
        buttons = [
            [KeyboardButton("🔍 Пошук героїв та гайдів"), KeyboardButton("🎙️ Голосовий пошук")],
            [KeyboardButton("📝 Історія пошуку"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("🔍 Оберіть опцію пошуку:", reply_markup=reply_markup)
        return States.SEARCH_PERFORMING
    elif user_input == "🆓 Початківець":
    buttons = [
        [KeyboardButton("👶 Початковий гайд"), KeyboardButton("📖 Базові поради")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("🆓 Оберіть опцію для початківців:", reply_markup=reply_markup)
    return States.BEGINNER_MENU

    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.MAIN_MENU
