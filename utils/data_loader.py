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
    # Шлях до вашого основного JSON-файлу з героями
    heroes_file = os.path.join('data', 'heroes', 'heroes.json')  # Переконайтесь, що файл називається 'heroes.json'
    
    if not os.path.exists(heroes_file):
        logger.error(f"Heroes file not found: {heroes_file}")
        return all_heroes

    data = load_json_data(heroes_file)
    if data and 'heroes' in data:
        for hero in data['heroes']:
            class_name = hero.get('class', 'Unknown')
            # Переконайтеся, що клас записаний англійською мовою
            # Якщо ні, розглянемо можливість перекладу або адаптації
            # Наприклад, якщо "Стрілець" → "Marksman"
            class_name = translate_class_name(class_name)

            if class_name not in all_heroes:
                all_heroes[class_name] = []
            all_heroes[class_name].append(hero)
    else:
        logger.error("No heroes found in the JSON file or 'heroes' key is missing.")
    
    logger.info(f"Loaded heroes: { {k: [h['name'] for h in v] for k, v in all_heroes.items()} }")
    return all_heroes

def translate_class_name(ukrainian_class_name):
    # Функція для перекладу назв класів з української на англійську
    translations = {
        "Танк": "Tank",
        "Стрілець": "Marksman",
        "Асасин": "Assassin",
        "Маг": "Mage",
        "Підтримка": "Support",
        # Додайте інші класи за потреби
    }
    return translations.get(ukrainian_class_name, "Unknown")
