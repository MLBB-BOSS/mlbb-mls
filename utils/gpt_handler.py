import openai
import os
import asyncio

async def handle_ai_query(prompt: str) -> str:
    """Відправляє запит до OpenAI API і повертає відповідь"""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # Отримання поточного циклу подій і виконання синхронного виклику у фоновому потоці
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,  # Використовує стандартний ThreadPoolExecutor
        lambda: openai.Completion.create(
            engine="text-davinci-003",  # або інший двигун, якщо вказано
            prompt=prompt,
            max_tokens=150
        )
    )
    return response.choices[0].text.strip()
