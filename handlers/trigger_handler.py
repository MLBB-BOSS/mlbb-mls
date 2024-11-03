# handlers/trigger_handler.py
from telegram import Update
from telegram.ext import ContextTypes
import random
import asyncio
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
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time
    message_text = update.message.text.lower()

    if any(trigger in message_text for trigger in TRIGGER_WORDS):
        personality = random.choice(list(PERSONALITY_RESPONSES.keys()))
        response = random.choice(PERSONALITY_RESPONSES[personality])

        await update.message.reply_text(response)

        # Додайте вашу логіку для генерації відповіді або інші дії
        
