# utils/data_loader.py
import json
import logging

logger = logging.getLogger(__name__)

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Помилка при завантаженні {file_path}: {e}")
        return {}
