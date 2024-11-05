# handlers/main_menu.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_all_heroes
import asyncio
import logging

logger = logging.getLogger(__name__)

# Завантаження всіх героїв
HEROES_BY_CLASS = load_all_heroes()

def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton("🦸 Герої")],
        # Ви можете додати інші кнопки за потребою
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    if user_input == "🦸 Герої":
        # Відображаємо клавіатуру з класами героїв
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
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.", reply_markup=reply_markup)
        return States.MAIN_MENU

