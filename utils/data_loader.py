# utils/data_loader.py
import os
import json

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        print(f"Error loading JSON data from {file_path}: {e}")
        return None

def load_all_heroes():
    all_heroes = {}
    heroes_dir = os.path.join('data', 'heroes')
    for class_dir in os.listdir(heroes_dir):
        class_path = os.path.join(heroes_dir, class_dir)
        if os.path.isdir(class_path):
            class_name = class_dir
            all_heroes[class_name] = []
            for hero_dir in os.listdir(class_path):
                hero_path = os.path.join(class_path, hero_dir)
                if os.path.isdir(hero_path):
                    # Очікуємо, що файл героя має назву hero_dir.json
                    hero_file = os.path.join(hero_path, f"{hero_dir}.json")
                    if os.path.exists(hero_file):
                        hero_data = load_json_data(hero_file)
                        if hero_data:
                            all_heroes[class_name].append(hero_data)
    return all_heroes
