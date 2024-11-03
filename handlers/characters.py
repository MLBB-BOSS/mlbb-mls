# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from handlers import States
from utils.data_loader import load_json_data
import asyncio  # Додано для використання asyncio
import logging

logger = logging.getLogger(__name__)

async def handle_characters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    logger.debug(f"Вибір в Персонажах: {user_input}")
     
    if user_input == "📝 Деталі про героїв":
        await send_character_details(update, context)
        return States.CHARACTERS_MENU

    elif user_input == "🧩 Вгадай героя":
        # Логіка для "Вгадай героя"
        await update.message.reply_text("Функція 'Вгадай героя' ще не реалізована.")
        return States.CHARACTERS_MENU

    elif user_input == "⚔️ Порівняння героїв":
        await send_character_comparison(update, context)
        return States.CHARACTERS_MENU

    elif user_input == "🎯 Контргерої":
        await send_counter_strategies(update, context)
        return States.CHARACTERS_MENU

    elif user_input == "🗂 Список героїв":
        await list_characters(update, context)
        return States.CHARACTERS_MENU

    elif user_input == "🔙 Назад":
        # Повернення до головного меню
        buttons = [
            [KeyboardButton("🧙‍♂️ Персонажі"), KeyboardButton("📚 Гайди")],
            [KeyboardButton("🏆 Турніри"), KeyboardButton("🔄 Оновлення")],
            [KeyboardButton("🆓 Початківець"), KeyboardButton("🔍 Пошук")],
            [KeyboardButton("📰 Новини"), KeyboardButton("💡 Допомога")],
            [KeyboardButton("🎮 Вікторини")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.CHARACTERS_MENU

async def send_character_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    character_details = (
        "📖 **Деталі про героя:**\n\n"
        "<b>Ім'я:</b> Джонсон\n"
        "<b>Клас:</b> Танки\n"
        "<b>Основні навички:</b> Навичка 1, Навичка 2, Навичка 3\n\n"
        "🔗 Детальніше: https://example.com/johnson-details"
    )
    await update.message.reply_text(character_details, parse_mode='HTML', disable_web_page_preview=True)

async def send_character_comparison(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    comparison = (
        "⚔️ **Порівняння героїв:**\n\n"
        "<b>Джонсон:</b> HP: 2000, Атака: 150, Захист: 300\n"
        "<b>Фрідом:</b> HP: 1800, Атака: 170, Захист: 250\n\n"
        "🔗 Детальніше: https://example.com/comparison"
    )
    await update.message.reply_text(comparison, parse_mode='HTML', disable_web_page_preview=True)

async def send_counter_strategies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    strategies = (
        "🎯 **Контргерої:**\n\n"
        "• Для контратаки Джонсон використовуйте Муну.\n"
        "• Для Фрідома найкраще підійдуть Анні.\n\n"
        "🔗 Детальніше: https://example.com/counter-strategies"
    )
    await update.message.reply_text(strategies, parse_mode='HTML', disable_web_page_preview=True)

async def list_characters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    heroes_data = load_json_data('data/characters.json')
    heroes = heroes_data.get('heroes', [])
    buttons = []
    for i in range(0, len(heroes), 4):
        row = heroes[i:i + 4]
        buttons.append([KeyboardButton(hero["name"]) for hero in row])
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("🗂 **Список героїв:**", parse_mode='Markdown', reply_markup=reply_markup)
    return States.CHARACTERS_MENU
    
