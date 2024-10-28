# scripts/process_heroes.py

import os
import json
import re
import logging

# Налаштування логування для відстеження процесу
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Шляхи до вхідної папки з текстовими файлами та вихідної папки для JSON файлів
INPUT_DIR = os.path.join('data', 'raw_heroes')
OUTPUT_DIR = os.path.join('data', 'heroes')

def parse_hero_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Розділення контенту на розділи для кожного героя
    hero_data = {}
    try:
        # Отримуємо ім'я героя
        hero_name_match = re.search(r"###\s\*\*(.*?)\*\*", content)
        hero_data['name'] = hero_name_match.group(1) if hero_name_match else "Невідомий"

        # Отримуємо роль
        role_match = re.search(r"\*\*Роль\*\*:\s(.*)", content)
        hero_data['role'] = role_match.group(1).split(" / ") if role_match else []

        # Отримуємо швидкість
        speed_match = re.search(r"\*\*Швидкість\*\*:\s(.*)", content)
        hero_data['speed'] = speed_match.group(1) if speed_match else "Невідомо"

        # Отримуємо здоров'я
        health_match = re.search(r"\*\*Здоров'я \(HP\)\*\*:\s(.*)", content)
        hero_data['health'] = health_match.group(1) if health_match else "Невідомо"

        # Отримуємо навички
        skills = {}
        skill_matches = re.findall(r"\d+\.\s+\*\*(.*?)\*\*:\s+(.*?)\n(?=\d+\.\s+\*\*|$)", content, re.DOTALL)
        for idx, (skill_name, skill_desc) in enumerate(skill_matches, start=1):
            # Розділення деталей навички
            cooldown = re.search(r"Час перезарядки:\s*([\d]+ секунд)", skill_desc)
            cooldown = cooldown.group(1) if cooldown else "Невідомо"
            mana_cost = re.search(r"Витрати мани:\s*(\d+)", skill_desc)
            mana_cost = int(mana_cost.group(1)) if mana_cost else 0

            skills[f'skill_{idx}'] = {
                'name': skill_name.strip(),
                'description': skill_desc.strip(),
                'cooldown': cooldown,
                'mana_cost': mana_cost
            }
        hero_data['skills'] = skills

    except Exception as e:
        logger.error(f"Помилка при обробці файлу {file_path}: {e}")

    return hero_data

def save_hero_data(hero_data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    hero_name = hero_data['name'].replace(' ', '_')
    file_path = os.path.join(OUTPUT_DIR, f"{hero_name}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(hero_data, f, ensure_ascii=False, indent=4)
    logger.info(f"Збережено: {file_path}")

def main():
    # Переконайтесь, що вихідна папка існує
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Обробка всіх файлів у папці `raw_heroes`
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(INPUT_DIR, filename)
            hero_data = parse_hero_file(file_path)
            if hero_data:
                save_hero_data(hero_data)

if __name__ == "__main__":
    main()
