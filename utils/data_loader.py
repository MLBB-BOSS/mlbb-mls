# utils/data_loader.py
import os
import json
import logging

logger = logging.getLogger(__name__)

def load_all_heroes():
    heroes_by_class = {}
    heroes_path = 'data/heroes'
    for class_name in os.listdir(heroes_path):
        class_path = os.path.join(heroes_path, class_name)
        if os.path.isdir(class_path):
            heroes_by_class[class_name] = []
            for hero_name in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_name)
                hero_file = os.path.join(hero_path, f"{hero_name}.json")
                if os.path.isfile(hero_file):
                    heroes_by_class[class_name].append(hero_name)
                else:
                    logger.warning(f"Hero file not found: {hero_file}")
        else:
            if class_name not in ['.gitkeep', '__init__.py']:
                logger.warning(f"Expected directory for class, but found file: {class_path}")
    return heroes_by_class

def load_heroes_data():
    heroes_data = {}
    heroes_path = 'data/heroes'
    for class_name in os.listdir(heroes_path):
        class_path = os.path.join(heroes_path, class_name)
        if os.path.isdir(class_path):
            for hero_name in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_name)
                hero_file = os.path.join(hero_path, f"{hero_name}.json")
                if os.path.isfile(hero_file):
                    try:
                        with open(hero_file, 'r', encoding='utf-8') as f:
                            hero_info = json.load(f)
                            heroes_data[hero_name] = hero_info
                    except Exception as e:
                        logger.error(f"Error loading hero data from {hero_file}: {e}")
                else:
                    logger.warning(f"Hero file not found: {hero_file}")
    return heroes_data
