# handlers/states.py
from enum import Enum, auto

class States(Enum):
    MAIN_MENU = auto()
    SELECTING_HERO_CLASS = auto()
    SELECTING_HERO = auto()
    HERO_FUNCTIONS_MENU = auto()
    # Додайте інші стани за потребою
