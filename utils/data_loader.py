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

# Функція для завантаження даних про борців
def load_fighter_data():
    """
    Завантажує дані з файлу fighter.json.
    """
    file_path = os.path.join('json', 'fighter.json')  # Виправлено шлях
    return load_json_data(file_path)

# Функція для завантаження даних про всіх героїв (якщо у вас є інші класи героїв у проекті)
def load_all_heroes():
    """
    Завантажує дані для всіх класів героїв.
    """
    all_heroes = {}

    # Додаємо дані борців
    fighters = load_fighter_data()
    if fighters:
        all_heroes['fighter'] = fighters.get('heroes', [])

    # Додайте інші класи за потреби
    # all_heroes['mage'] = load_mage_data()
    # all_heroes['tank'] = load_tank_data()
    # ...

    return all_heroes
