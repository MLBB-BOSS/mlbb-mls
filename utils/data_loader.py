# utils/data_loader.py
import json
import os
import logging

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

def load_fighter_data():
    """
    Завантажує дані з файлу fighter.json.
    """
    file_path = os.path.join('data', 'heroes', 'fighter.json')  # Оновлений шлях
    return load_json_data(file_path)

def load_mage_data():
    """
    Завантажує дані з файлу mage.json.
    """
    file_path = os.path.join('data', 'heroes', 'mage.json')  # Оновлений шлях
    return load_json_data(file_path)

def load_marksmen_data():
    """
    Завантажує дані з файлу marksmen.json.
    """
    file_path = os.path.join('data', 'heroes', 'marksmen.json')  # Оновлений шлях
    return load_json_data(file_path)

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

    # Додаємо дані стрільців
    marksmen = load_marksmen_data()
    if marksmen:
        all_heroes['Стрілець'] = marksmen.get('heroes', [])

    # Додайте інші класи за потреби

    return all_heroes
