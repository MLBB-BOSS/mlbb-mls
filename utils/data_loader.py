# utils/data_loader.py
import os
import json
import logging

logger = logging.getLogger(__name__)

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        logger.error(f"Error loading JSON data from {file_path}: {e}")
        return None

def load_all_heroes():
    all_heroes = {}
    heroes_dir = os.path.join('data', 'heroes')
    for class_dir in os.listdir(heroes_dir):
        class_path = os.path.join(heroes_dir, class_dir)
        if os.path.isdir(class_path):
            class_name = class_dir  # Ensure class_name matches "Tank", "Assassin", etc.
            all_heroes[class_name] = []
            for hero_dir in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_dir)
                if os.path.isdir(hero_path):
                    hero_file = os.path.join(hero_path, f"{hero_dir}.json")
                    if os.path.exists(hero_file):
                        hero_data = load_json_data(hero_file)
                        if hero_data:
                            all_heroes[class_name].append(hero_data)
                        else:
                            logger.warning(f"Failed to load hero data for {hero_dir}")
                    else:
                        logger.warning(f"Hero file not found: {hero_file}")
                else:
                    logger.warning(f"Expected directory for hero, but found file: {hero_path}")
        else:
            logger.warning(f"Expected directory for class, but found file: {class_path}")
    logger.info(f"Loaded heroes: { {k: [h['name'] for h in v] for k, v in all_heroes.items()} }")
    return all_heroes
