# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"

# Перевірка наявності ключів
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено в змінних оточення.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не встановлено в змінних оточення.")
