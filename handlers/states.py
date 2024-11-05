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
    GUIDES_MENU = auto()
    TOURNAMENTS_MENU = auto()
    UPDATES_MENU = auto()
    BEGINNER_MENU = auto()
    NEWS_MENU = auto()
    HELP_MENU = auto()
    QUIZZES_MENU = auto()
    SEARCH_MENU = auto()
    SEARCH_PERFORMING = auto()
    SEARCH_HERO_GUIDES = auto()
    COMPARISONS_MENU = auto()
    EMBLEMS_MENU = auto()
    ITEMS_MENU = auto()
    RECOMMENDATIONS_MENU = auto()
    # Додайте інші стани за потребою
