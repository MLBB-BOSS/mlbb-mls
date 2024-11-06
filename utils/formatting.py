# utils/formatting.py

import re

def format_ai_response(ai_text: str) -> str:
    """
    Функція для форматування відповіді AI перед відправкою користувачу.
    
    Args:
        ai_text (str): Відповідь від AI.
    
    Returns:
        str: Відформатована відповідь.
    """
    # Видалення зайвих пробілів на початку та в кінці
    formatted_text = ai_text.strip()
    
    # Видалення зайвих пробілів між рядками
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    
    return formatted_text
