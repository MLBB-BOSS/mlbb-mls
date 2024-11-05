# handlers/states.py
from enum import Enum

class States(Enum):
    MAIN_MENU = 0
    SELECTING_HERO_CLASS = 1
    SELECTING_HERO = 2
    HERO_FUNCTIONS_MENU = 3
    PROFILE_MENU = 4
    # Додайте інші стани за потреби
