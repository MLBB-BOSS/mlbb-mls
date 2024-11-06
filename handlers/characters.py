# handlers/characters.py

import openai
import logging
from telegram.ext import ContextTypes
from utils.formatting import format_ai_response  # Імпорт функції форматування

# Налаштування логування
logger = logging.getLogger(__name__)

async def get_hero_info(hero_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Функція для отримання детальної інформації про героя через OpenAI API.

    Args:
        hero_name (str): Назва героя.
        context (ContextTypes.DEFAULT_TYPE): Контекст Telegram бота.

    Returns:
        str: Детальна інформація про героя або повідомлення про помилку.
    """
    try:
        # Отримання базової інформації про героя
        heroes_data = context.bot_data.get('heroes_data', {})
        hero_info = heroes_data.get(hero_name)

        if not hero_info:
            return "⚠️ Не вдалося знайти інформацію про цього героя."

        # Отримання класу героя для кешування
        hero_class = hero_info.get('class', 'Unknown')

        # Створення системного промпту
        system_prompt = (
            "Ти — інформативний і дружній помічник Telegram-бота для надання "
            "інформації про героїв гри Mobile Legends: Bang Bang. "
            "Відповідай лаконічно, використовуючи українську мову. "
            "Використовуй надану базову інформацію про героя для створення повного опису."
        )

        # Створення промпту на основі базової інформації
        base_info = (
            f"Ім'я героя: {hero_info.get('name', 'Невідомо')}\n"
            f"Клас: {hero_info.get('class', 'N/A')}\n"
            f"Роль: {hero_info.get('role', 'N/A')}\n"
            f"Швидкість: {hero_info.get('speed', 'N/A')}\n"
            f"Здоров'я (HP): {hero_info.get('hp', 'N/A')}\n"
            f"Мана (MP): {hero_info.get('mp', 'N/A')}\n"
            f"Фізичний захист: {hero_info.get('physical_defense', 'N/A')}\n"
            f"Магічний захист: {hero_info.get('magical_defense', 'N/A')}\n"
            f"Швидкість атаки: {hero_info.get('attack_speed', 'N/A')}\n\n"
            "Навички:\n"
        )

        skills = hero_info.get('skills', {})
        for skill_type in ['passive', 'skill1', 'skill2', 'ultimate']:
            skill = skills.get(skill_type)
            if skill:
                info = (
                    f"{skill_type.capitalize()}: {skill.get('name', 'N/A')}\n"
                    f"Опис: {skill.get('description', 'N/A')}\n"
                    f"Час перезарядки: {skill.get('cooldown', 'N/A')}\n"
                    f"Витрати мани: {skill.get('mana_cost', 'N/A')}\n\n"
                )
                base_info += info

        strategies = hero_info.get('strategies', {})
        recommendations = hero_info.get('recommendations', {})
        drafts = hero_info.get('drafts', {})

        base_info += (
            "Стратегії:\n"
            f"• Агресивна стратегія: {strategies.get('aggressive', 'N/A')}\n"
            f"• Захисна стратегія: {strategies.get('defensive', 'N/A')}\n"
            f"• Мікрогра: {strategies.get('micro', 'N/A')}\n\n"
            "Рекомендації щодо гри:\n"
            f"• Ранній етап: {recommendations.get('early_game', 'N/A')}\n"
            f"• Середній етап: {recommendations.get('mid_game', 'N/A')}\n"
            f"• Пізня гра: {recommendations.get('late_game', 'N/A')}\n\n"
            "Драфти:\n"
            f"• Ідеальні союзники: {drafts.get('ideal_allies', 'N/A')}\n"
            f"• Кого краще уникати: {drafts.get('avoid_enemies', 'N/A')}\n"
            f"• Сильні драфти: {drafts.get('strong_drafts', 'N/A')}\n"
        )

        # Формування повного промпту
        user_prompt = (
            "На основі наступної базової інформації, створіть повний опис героя Mobile Legends: Bang Bang. "
            "Використовуйте надані дані та додайте свої рекомендації щодо стратегії та гри.\n\n"
            f"{base_info}"
        )

        # Перевірка наявності кешованої відповіді
        cache = context.bot_data.get('ai_responses', {})
        cache_key = f"{hero_name}_{hero_class}"
        if cache_key in cache:
            logger.info(f"Отримано дані з кешу для {hero_name} ({hero_class})")
            return cache[cache_key]

        # Виклик OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        ai_text = response.choices[0].message['content'].strip()

        # Форматуємо відповідь для Telegram
        formatted_text = format_ai_response(ai_text)  # Переконайтеся, що функція format_ai_response існує

        # Зберігаємо в кеш
        cache[cache_key] = formatted_text
        context.bot_data['ai_responses'] = cache

        logger.info(f"Відповідь від AI успішно отримана для героя: {hero_name}")

        return formatted_text

    except Exception as e:
        logger.error(f"Помилка під час отримання інформації про героя: {e}")
        return "⚠️ Виникла помилка при обробці запиту. Спробуйте пізніше."
    ```

### Оновлення `utils/openai_api.py`

Якщо ви використовували `handle_gpt_query` у вашому проекті, переконайтеся, що ви імпортуєте його з правильного місця. Якщо ви дотримуєтеся попередніх рекомендацій щодо розміщення функцій, ось приклад, як може виглядати файл `utils/openai_api.py`:

```python
# utils/openai_api.py

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
        
