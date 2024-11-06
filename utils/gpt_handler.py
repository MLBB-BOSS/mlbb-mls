# utils/gpt_handler.py

import openai
import os

async def handle_ai_query(prompt: str) -> str:
    """Відправляє запит до OpenAI API і повертає відповідь"""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine="text-davinci-003",  # або інший двигун, якщо вказано
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
