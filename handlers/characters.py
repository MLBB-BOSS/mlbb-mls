# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_json_data
import asyncio
import logging

logger = logging.getLogger(__name__)

async def handle_characters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    logger.debug(f"Вибір у Героях: {user_input}")

    if user_input == "⚔️ Порівняння героїв":
        await update.message.reply_text("Оберіть першого героя для порівняння:")
        await list_heroes(update, context)
        return States.COMPARISON_FIRST_HERO

    elif user_input == "🎯 Контргерої":
        await update.message.reply_text("Оберіть героя, для якого хочете дізнатися контр-героїв:")
        await list_heroes(update, context)
        return States.SELECTING_COUNTER_HERO

    elif user_input == "🗂 Список героїв":
        classes = ['Танк', 'Маг', 'Стрілець', 'Підтримка', 'Борець', 'Убивця']
        buttons = [[KeyboardButton(cls)] for cls in classes]
        buttons.append([KeyboardButton("🔙 Назад")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("Оберіть клас героя:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS

    elif user_input == "🔙 Назад":
        from handlers.start_handler import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    else:
        await update.message.reply_text("⚠️ Будь ласка, оберіть опцію з меню.")
        return States.CHARACTERS_MENU

async def list_heroes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    heroes_data = load_json_data('data/characters.json')
    heroes = heroes_data.get('heroes', [])
    buttons = []
    for i in range(0, len(heroes), 4):
        row = heroes[i:i + 4]
        buttons.append([KeyboardButton(hero["name"]) for hero in row])
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Оберіть героя:", reply_markup=reply_markup)

async def handle_comparison_first_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    first_hero = update.message.text.strip()
    context.user_data['first_hero'] = first_hero
    await update.message.reply_text(f"Ви обрали {first_hero}. Тепер оберіть другого героя для порівняння:")
    await list_heroes(update, context)
    return States.COMPARISON_SECOND_HERO

async def handle_comparison_second_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    second_hero = update.message.text.strip()
    first_hero = context.user_data.get('first_hero')
    comparison_result = compare_heroes(first_hero, second_hero)
    await update.message.reply_text(comparison_result, parse_mode='HTML')
    return States.CHARACTERS_MENU

def compare_heroes(hero1_name: str, hero2_name: str) -> str:
    heroes_data = load_json_data('data/characters.json')
    hero1 = next((hero for hero in heroes_data['heroes'] if hero['name'] == hero1_name), None)
    hero2 = next((hero for hero in heroes_data['heroes'] if hero['name'] == hero2_name), None)
    if not hero1 or not hero2:
        return "Не вдалося знайти одного або обох героїв."
    comparison = f"""
⚔️ <b>Порівняння героїв:</b>

<b>{hero1['name']}:</b> HP: {hero1['hp']}, Атака: {hero1['attack']}, Захист: {hero1['defense']}
<b>{hero2['name']}:</b> HP: {hero2['hp']}, Атака: {hero2['attack']}, Захист: {hero2['defense']}
"""
    return comparison

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    context.user_data['selected_class'] = selected_class
    heroes_data = load_json_data('data/characters.json')
    heroes = [hero['name'] for hero in heroes_data['heroes'] if hero['class'] == selected_class]
    if not heroes:
        await update.message.reply_text("Не знайдено героїв цього класу.")
        return States.CHARACTERS_MENU
    buttons = [[KeyboardButton(hero)] for hero in heroes]
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Оберіть героя класу {selected_class}:", reply_markup=reply_markup)
    return States.SELECTING_HERO

async def handle_selecting_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    heroes_data = load_json_data('data/characters.json')
    hero = next((hero for hero in heroes_data['heroes'] if hero['name'] == hero_name), None)
    if not hero:
        await update.message.reply_text("Не вдалося знайти інформацію про цього героя.")
        return States.CHARACTERS_MENU
    hero_details = f"""
📖 <b>Деталі про героя:</b>

<b>Ім'я:</b> {hero['name']}
<b>Клас:</b> {hero['class']}
<b>Основні навички:</b> {', '.join(hero['skills'])}

🔗 Детальніше: {hero.get('details_url', 'Немає інформації')}
"""
    await update.message.reply_text(hero_details, parse_mode='HTML')
    return States.CHARACTERS_MENU

async def handle_selecting_counter_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    counters_data = load_json_data('data/counters.json')
    counters = counters_data.get(hero_name)
    if not counters:
        await update.message.reply_text("Не вдалося знайти контр-героїв для цього героя.")
        return States.CHARACTERS_MENU
    counters_list = '\n'.join(f"• {counter}" for counter in counters)
    response = f"""
🎯 <b>Контр-герої для {hero_name}:</b>

{counters_list}
"""
    await update.message.reply_text(response, parse_mode='HTML')
    return States.CHARACTERS_MENU
