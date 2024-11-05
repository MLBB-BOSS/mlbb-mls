# utils/data_loader.py

import json
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def load_all_heroes() -> Dict[str, list]:
    heroes_by_class = {}
    heroes_path = 'data/heroes'
    for class_name in os.listdir(heroes_path):
        class_path = os.path.join(heroes_path, class_name)
        if os.path.isdir(class_path):
            heroes_by_class[class_name] = []
            for hero_name in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_name)
                if os.path.isdir(hero_path):
                    # Шукаємо JSON-файл у директорії героя
                    json_files = [f for f in os.listdir(hero_path) if f.endswith('.json')]
                    if json_files:
                        heroes_by_class[class_name].append(hero_name)
                    else:
                        logger.warning(f"JSON-файл не знайдено для героя: {hero_name}")
                else:
                    logger.warning(f"Очікувалась директорія для героя, але знайдено файл: {hero_path}")
            if not heroes_by_class[class_name]:
                logger.warning(f"Немає героїв у класі: {class_name}")
        else:
            logger.warning(f"Очікувалась директорія для класу, але знайдено файл: {class_path}")
    return heroes_by_class

def load_heroes_data() -> Dict[str, dict]:
    heroes_data = {}
    heroes_path = 'data/heroes'
    for class_name in os.listdir(heroes_path):
        class_path = os.path.join(heroes_path, class_name)
        if os.path.isdir(class_path):
            for hero_name in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_name)
                if os.path.isdir(hero_path):
                    # Шукаємо JSON-файл у директорії героя
                    json_files = [f for f in os.listdir(hero_path) if f.endswith('.json')]
                    if json_files:
                        hero_file = os.path.join(hero_path, json_files[0])
                        try:
                            with open(hero_file, 'r', encoding='utf-8') as f:
                                hero_info = json.load(f)
                                heroes_data[hero_name] = hero_info
                        except Exception as e:
                            logger.error(f"Помилка завантаження даних героя з {hero_file}: {e}")
                    else:
                        logger.warning(f"JSON-файл не знайдено для героя: {hero_name}")
                else:
                    logger.warning(f"Очікувалась директорія для героя, але знайдено файл: {hero_path}")
    return heroes_data
