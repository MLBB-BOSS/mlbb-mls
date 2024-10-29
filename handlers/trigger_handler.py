# handlers/trigger_handler.py
from telegram import Update
from telegram.ext import ContextTypes
import random
from utils.openai_api import get_openai_response
import logging

logger = logging.getLogger(__name__)

TRIGGER_WORDS = ["бот", "GPT", "допоможи", "розкажи"]

PERSONALITY_RESPONSES = {
    "жартівливий": [
        "😂 Оце так запитання!",
        "😄 Ти мене розсмішив!",
        "🤣 Зараз я спробую..."
    ],
    "саркастичний": [
        "Ну звичайно, я ж робот.",
        "Що ж, ще одне геніальне питання.",
        "Ой, безмежно цікаво..."
    ],
    "підбадьорюючий": [
        "Все буде добре!",
        "Не хвилюйся, я тут, щоб допомогти.",
        "Разом ми це подолаємо!"
    ]
}

async def trigger_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    message_text = update.message.text.lower()

    if any(trigger in message_text for trigger in TRIGGER_WORDS):
        # Вибір випадкового типу відповіді
        personality = random.choice(list(PERSONALITY_RESPONSES.keys()))
        response = random.choice(PERSONALITY_RESPONSES[personality])
        
        await update.message.reply_text(response)
        
        # Генерація відповіді від GPT-4
        gpt_response = await get_openai_response(update.message.text)
        await update.message.reply_text(gpt_response, parse_mode='Markdown')
