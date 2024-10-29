# handlers/__init__.py
from enum import Enum, auto

class States(Enum):
    MAIN_MENU = auto()
    CHARACTERS_MENU = auto()
    GUIDES_MENU = auto()
    TOURNAMENTS_MENU = auto()
    UPDATES_MENU = auto()
    BEGINNER_MENU = auto()
    NEWS_MENU = auto()
    HELP_MENU = auto()
    QUIZZES_MENU = auto()
    SEARCH_PERFORMING = auto()
    SEARCH_HERO_GUIDES = auto()
    TANK_CHARACTERS_MENU = auto()
    # Додайте інші стани тут за потребою
