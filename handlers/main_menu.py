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
        [KeyboardButton("🦸 Heroes")],
        # Add other buttons as needed
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    if user_input == "🦸 Heroes":
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
        buttons.append([KeyboardButton("🔙 Back")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("Select a hero class:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS
    else:
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("⚠️ Please select an option from the menu.", reply_markup=reply_markup)
        return States.MAIN_MENU
