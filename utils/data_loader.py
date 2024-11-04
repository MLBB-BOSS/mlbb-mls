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

# Функція для завантаження даних про магів
def load_mage_data():
    """
    Завантажує дані з файлу mage.json.
    """
    file_path = os.path.join('json', 'mage.json')
    return load_json_data(file_path)

# Функція для завантаження даних про танків
def load_tank_data():
    """
    Завантажує дані з файлу heroes_tanks.json.
    """
    file_path = os.path.join('json', 'heroes_tanks.json')  # Можливо, необхідно уточнити назву файлу
    return load_json_data(file_path)

# Функція для завантаження даних про всіх героїв
def load_all_heroes():
    """
    Завантажує дані для всіх класів героїв.
    """
    all_heroes = {}

    # Додаємо дані борців
    fighters = load_fighter_data()
    if fighters:
        all_heroes['Борець'] = fighters.get('heroes', [])

    # Додаємо дані магів
    mages = load_mage_data()
    if mages:
        all_heroes['Маг'] = mages.get('heroes', [])

    # Додаємо дані танків
    tanks = load_tank_data()
    if tanks:
        all_heroes['Танк'] = tanks.get('heroes', [])

    # Додайте інші класи за потреби

    return all_heroes
