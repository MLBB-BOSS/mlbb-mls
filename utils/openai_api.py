# utils/openai_api.py
import aiohttp
import logging
from config.settings import OPENAI_API_KEY, API_URL

logger = logging.getLogger(__name__)

async def get_openai_response(user_input: str) -> str:
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 1200
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"Відправляємо запит до OpenAI API з повідомленням: {user_input}")
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    reply_text = response_data['choices'][0]['message']['content']
                    logger.info(f"Отримана відповідь від OpenAI API: {reply_text}")
                    return reply_text
                else:
                    error_text = await response.text()
                    logger.error(f"API Error: {response.status} - {error_text}")
                    return "⚠️ Сталася помилка при зверненні до API. Спробуйте ще раз."
    except Exception as e:
        logger.error(f"Невідома помилка: {e}")
        return "⚠️ Вибачте, сталася невідома помилка. Спробуйте знову."
