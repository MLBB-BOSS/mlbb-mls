# utils/data_loader.py
import json
import os
import logging

# Ініціалізація логування
logger = logging.getLogger(__name__)

def load_json_data(file_path):
    """
    Завантажує дані з JSON-файлу за заданим шляхом.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Успішно завантажено дані з {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не знайдено.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Помилка декодування JSON у файлі {file_path}.")
        return None

def load_hero_data(class_name, hero_name):
    """
    Завантажує дані про конкретного героя з відповідної папки.
    """
    file_name = f"{hero_name.lower().replace(' ', '_')}.json"
    file_path = os.path.join('data', 'heroes', class_name, file_name)
    return load_json_data(file_path)

def load_all_heroes():
    """
    Завантажує дані для всіх класів героїв.
    """
    all_heroes = {}

    heroes_dir = os.path.join('data', 'heroes')
    for class_dir in os.listdir(heroes_dir):
        class_path = os.path.join(heroes_dir, class_dir)
        if os.path.isdir(class_path):
            all_heroes[class_dir] = []
            for hero_file in os.listdir(class_path):
                if hero_file.endswith('.json'):
                    hero_data = load_json_data(os.path.join(class_path, hero_file))
                    if hero_data:
                        all_heroes[class_dir].append(hero_data)

    return all_heroes
