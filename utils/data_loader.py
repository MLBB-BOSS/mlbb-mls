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
    for filename in os.listdir(heroes_dir):
        if filename.endswith('.json'):
            hero_file = os.path.join(heroes_dir, filename)
            hero_data = load_json_data(hero_file)
            if hero_data:
                hero_class = hero_data.get('class', 'Unknown')
                if hero_class not in all_heroes:
                    all_heroes[hero_class] = []
                all_heroes[hero_class].append(hero_data)
    return all_heroes
