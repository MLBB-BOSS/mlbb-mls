# utils/data_loader.py

import json
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

def load_all_heroes() -> Dict[str, List[str]]:
    """
    Завантажує список всіх героїв, класифікованих за класами.

    Returns:
        Dict[str, List[str]]: Словник, де ключі — назви класів, а значення — списки героїв цього класу.
    """
    heroes_by_class = {}
    heroes_path = Path('data') / 'heroes'

    if not heroes_path.exists():
        logger.error(f"Шлях до героїв не існує: {heroes_path}")
        return heroes_by_class

    for class_dir in heroes_path.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            heroes_by_class[class_name] = []
            for hero_dir in class_dir.iterdir():
                if hero_dir.is_dir():
                    json_files = list(hero_dir.glob('*.json'))
                    if json_files:
                        # Припускаємо, що кожен герой має тільки один JSON-файл
                        heroes_by_class[class_name].append(hero_dir.name)
                    else:
                        logger.warning(f"JSON-файл не знайдено для героя: {hero_dir.name} в класі: {class_name}")
                else:
                    logger.warning(f"Очікувалась директорія для героя, але знайдено файл: {hero_dir}")
            if not heroes_by_class[class_name]:
                logger.warning(f"Немає героїв у класі: {class_name}")
        else:
            logger.warning(f"Очікувалась директорія для класу, але знайдено файл: {class_dir}")

    return heroes_by_class

def load_heroes_data() -> Dict[str, dict]:
    """
    Завантажує детальну інформацію про кожного героя з JSON-файлів.

    Returns:
        Dict[str, dict]: Словник з детальною інформацією про героїв.
    """
    heroes_data = {}
    heroes_path = Path('data') / 'heroes'

    if not heroes_path.exists():
        logger.error(f"Шлях до героїв не існує: {heroes_path}")
        return heroes_data

    for class_dir in heroes_path.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            for hero_dir in class_dir.iterdir():
                if hero_dir.is_dir():
                    json_files = list(hero_dir.glob('*.json'))
                    if json_files:
                        # Припускаємо, що кожен герой має тільки один JSON-файл
                        hero_file = json_files[0]
                        try:
                            with hero_file.open('r', encoding='utf-8') as f:
                                hero_info = json.load(f)
                                # Додаємо інформацію про клас до даних героя
                                hero_info['class'] = class_name
                                heroes_data[hero_dir.name] = hero_info
                        except json.JSONDecodeError as jde:
                            logger.error(f"JSONDecodeError при завантаженні даних героя з {hero_file}: {jde}")
                        except Exception as e:
                            logger.error(f"Помилка завантаження даних героя з {hero_file}: {e}")
                    else:
                        logger.warning(f"JSON-файл не знайдено для героя: {hero_dir.name} в класі: {class_name}")
                else:
                    logger.warning(f"Очікувалась директорія для героя, але знайдено файл: {hero_dir}")
        else:
            logger.warning(f"Очікувалась директорія для класу, але знайдено файл: {class_dir}")

    return heroes_data
    
