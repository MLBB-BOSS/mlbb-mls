# utils/keyboards.py

from telegram import ReplyKeyboardMarkup
from utils.data_loader import load_all_heroes

def get_hero_classes_keyboard() -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для вибору класу героїв.

    Returns:
        ReplyKeyboardMarkup: Клавіатура з кнопками класів героїв.
    """
    heroes_by_class = load_all_heroes()
    classes = list(heroes_by_class.keys())

    # Створюємо кнопки по 2 класи на рядок
    keyboard = [classes[i:i + 2] for i in range(0, len(classes), 2)]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
  
