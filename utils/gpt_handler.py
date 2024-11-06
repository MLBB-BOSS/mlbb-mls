# utils/gpt_handler.py

import logging
from handlers.characters import get_hero_info
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def handle_gpt_query(hero_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Функція для обробки запиту до GPT для отримання інформації про героя.

    Args:
        hero_name (str): Назва героя.
        context (ContextTypes.DEFAULT_TYPE): Контекст Telegram бота.

    Returns:
        str: Відповідь від GPT або повідомлення про помилку.
    """
    return await get_hero_info(hero_name, context)
  
