# handlers/comparisons.py

from telegram import Update
from telegram.ext import ContextTypes
from handlers import States
from utils.data_loader import load_json_data
import logging

logger = logging.getLogger(__name__)

async def handle_comparisons_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір у Порівняннях: {user_input}")

    if user_input == "🔙 Назад":
        from handlers.characters import handle_characters_menu
        await handle_characters_menu(update, context)
        return States.CHARACTERS_MENU
    else:
        # Логіка для обробки порівняння героїв
        await send_character_comparison(update, context)
        return States.COMPARISONS_MENU

async def send_character_comparison(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Приклад простої функції порівняння героїв
    hero1 = "Джонсон"
    hero2 = "Фрідом"

    # Отримуємо дані про героїв з файлу
    heroes_data = load_json_data('data/characters.json').get('heroes', [])
    hero1_data = next((hero for hero in heroes_data if hero['name'] == hero1), None)
    hero2_data = next((hero for hero in heroes_data if hero['name'] == hero2), None)

    if hero1_data and hero2_data:
        comparison = (
            f"⚔️ **Порівняння героїв:**\n\n"
            f"<b>{hero1_data['name']}:</b> HP: {hero1_data['hp']}, Атака: {hero1_data['attack']}, Захист: {hero1_data['defense']}\n"
            f"<b>{hero2_data['name']}:</b> HP: {hero2_data['hp']}, Атака: {hero2_data['attack']}, Захист: {hero2_data['defense']}\n\n"
            f"🔗 Детальніше: https://example.com/comparison"
        )
        await update.message.reply_text(comparison, parse_mode='HTML', disable_web_page_preview=True)
    else:
        await update.message.reply_text("Не вдалося знайти інформацію про одного з героїв.")
