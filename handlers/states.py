# handlers/states.py
from enum import Enum, auto

class States(Enum):
    MAIN_MENU = auto()
    CHARACTERS_MENU = auto()
    SELECTING_HERO_CLASS = auto()
    SELECTING_HERO = auto()
    HERO_FUNCTIONS_MENU = auto()
    COMPARISON_FIRST_HERO = auto()
    COMPARISON_SECOND_HERO = auto()
    SELECTING_COUNTER_HERO = auto()
    # Видаляємо стани, для яких немає обробників
    # Додайте інші стани за потребою
