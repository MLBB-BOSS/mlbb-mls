# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_fighter_data
import asyncio
import logging
import json
import os

logger = logging.getLogger(__name__)

# Завантаження героїв класу "Борець" з файлу fighter.json
fighter_data_path = os.path.join('json', 'fighter.json')  # Переконайтеся, що шлях правильний
fighter_data = load_fighter_data()

if fighter_data:
    HEROES_BY_CLASS = {
        'Борець': [hero['name'] for hero in fighter_data['heroes']],
        'Танк': [
            'Akai', 'Atlas', 'Barats', 'Baxia', 'Belerick', 'Franco',
            'Gatotkaca', 'Gloo', 'Grock', 'Hylos', 'Johnson', 'Khufra',
            'Lolita', 'Minotaur', 'Masha', 'Tigreal', 'Uranus', 'Edith', 'Fredrinn'
        ],
        'Маг': [
            'Alice', 'Aurora', 'Cecilion', 'Chang\'e', 'Cyclops', 'Esmeralda',
            'Eudora', 'Gord', 'Harley', 'Kadita', 'Kagura', 'Kimmy', 'Lunox',
            'Lylia', 'Nana', 'Odette', 'Pharsa', 'Vale', 'Valentina', 'Vexana',
            'Xavier', 'Yve', 'Zhask', 'Zhuxin'
        ],
        'Стрілець': [
            'Beatrix', 'Brody', 'Bruno', 'Claude', 'Clint', 'Dyrroth', 'Granger',
            'Hanabi', 'Hilda', 'Irithel', 'Karrie', 'Kimmy', 'Layla', 'Lesley',
            'Martis', 'Melissa', 'Miya', 'Moskov', 'Natan', 'Popol and Kupa',
            'Wanwan', 'Yi Sun-Shin'
        ],
        'Підтримка': [
            'Angela', 'Carmilla', 'Chip', 'Diggie', 'Estes', 'Faramis', 'Floryn',
            'Kaja', 'Mathilda', 'Nana', 'Rafaela'
        ],
        'Убивця': [
            'Aamon', 'Benedetta', 'Fanny', 'Gusion', 'Hanzo', 'Helcurt', 'Joy',
            'Julian', 'Karina', 'Lancelot', 'Ling', 'Natalia', 'Saber', 'Selena'
        ]
    }
else:
    logger.error("Дані про борців не завантажені. Перевірте файл fighter.json.")
    HEROES_BY_CLASS = {
        'Борець': [],
        'Танк': [
            'Akai', 'Atlas', 'Barats', 'Baxia', 'Belerick', 'Franco',
            'Gatotkaca', 'Gloo', 'Grock', 'Hylos', 'Johnson', 'Khufra',
            'Lolita', 'Minotaur', 'Masha', 'Tigreal', 'Uranus', 'Edith', 'Fredrinn'
        ],
        'Маг': [
            'Alice', 'Aurora', 'Cecilion', 'Chang\'e', 'Cyclops', 'Esmeralda',
            'Eudora', 'Gord', 'Harley', 'Kadita', 'Kagura', 'Kimmy', 'Lunox',
            'Lylia', 'Nana', 'Odette', 'Pharsa', 'Vale', 'Valentina', 'Vexana',
            'Xavier', 'Yve', 'Zhask', 'Zhuxin'
        ],
        'Стрілець': [
            'Beatrix', 'Brody', 'Bruno', 'Claude', 'Clint', 'Dyrroth', 'Granger',
            'Hanabi', 'Hilda', 'Irithel', 'Karrie', 'Kimmy', 'Layla', 'Lesley',
            'Martis', 'Melissa', 'Miya', 'Moskov', 'Natan', 'Popol and Kupa',
            'Wanwan', 'Yi Sun-Shin'
        ],
        'Підтримка': [
            'Angela', 'Carmilla', 'Chip', 'Diggie', 'Estes', 'Faramis', 'Floryn',
            'Kaja', 'Mathilda', 'Nana', 'Rafaela'
        ],
        'Убивця': [
            'Aamon', 'Benedetta', 'Fanny', 'Gusion', 'Hanzo', 'Helcurt', 'Joy',
            'Julian', 'Karina', 'Lancelot', 'Ling', 'Natalia', 'Saber', 'Selena'
        ]
    }

def get_characters_menu_keyboard():
    buttons = [
        [KeyboardButton("⚔️ Порівняння героїв"), KeyboardButton("🎯 Контргерої")],
        [KeyboardButton("🗂 Список героїв")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def handle_characters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id
    current_time = asyncio.get_running_loop().time()
    context.bot_data['last_message_time'][user_id] = current_time

    if user_input == "⚔️ Порівняння героїв":
        await update.message.reply_text("Оберіть першого героя для порівняння:")
        await list_all_heroes(update, context)
        return States.COMPARISON_FIRST_HERO

    elif user_input == "🎯 Контргерої":
        await update.message.reply_text("Оберіть героя, для якого хочете дізнатися контр-героїв:")
        await list_all_heroes(update, context)
        return States.SELECTING_COUNTER_HERO

    elif user_input == "🗂 Список героїв":
        classes = list(HEROES_BY_CLASS.keys())
        buttons = []
        for cls in classes:
            buttons.append([KeyboardButton(cls)])
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
        reply_markup = get_characters_menu_keyboard()
        await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
        return States.CHARACTERS_MENU

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    if selected_class == "🔙 Назад":
        reply_markup = get_characters_menu_keyboard()
        await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
        return States.CHARACTERS_MENU

    if selected_class not in HEROES_BY_CLASS:
        await update.message.reply_text("⚠️ Будь ласка, оберіть клас з меню.")
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = HEROES_BY_CLASS[selected_class]
    buttons = []
    row = []
    for idx, hero in enumerate(heroes, 1):
        row.append(KeyboardButton(hero))
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Оберіть героя класу {selected_class}:", reply_markup=reply_markup)
    return States.SELECTING_HERO

async def handle_selecting_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    if hero_name == "🔙 Назад":
        return await handle_selecting_hero_class(update, context)

    selected_class = context.user_data.get('selected_class')
    if selected_class is None or hero_name not in HEROES_BY_CLASS.get(selected_class, []):
        await update.message.reply_text("⚠️ Будь ласка, оберіть героя з меню.")
        return States.SELECTING_HERO

    context.user_data['selected_hero'] = hero_name

    buttons = [
        [KeyboardButton("ℹ️ Загальна інформація"), KeyboardButton("🎯 Контрпіки")],
        [KeyboardButton("📖 Гайди"), KeyboardButton("🗺️ Стратегії")],
        [KeyboardButton("⚔️ Порівняння"), KeyboardButton("🛠️ Білди")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Ви обрали героя {hero_name}. Оберіть опцію:", reply_markup=reply_markup)
    return States.HERO_FUNCTIONS_MENU

async def handle_comparison_first_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    first_hero = update.message.text.strip()
    context.user_data['first_hero'] = first_hero

    all_heroes = [hero for heroes in HEROES_BY_CLASS.values() for hero in heroes]
    if first_hero not in all_heroes:
        await update.message.reply_text("⚠️ Будь ласка, оберіть героя з меню.")
        return States.COMPARISON_FIRST_HERO

    await update.message.reply_text(f"Ви обрали {first_hero}. Тепер оберіть другого героя для порівняння:")
    await list_all_heroes(update, context)
    return States.COMPARISON_SECOND_HERO

async def handle_comparison_second_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    second_hero = update.message.text.strip()
    first_hero = context.user_data.get('first_hero')

    all_heroes = [hero for heroes in HEROES_BY_CLASS.values() for hero in heroes]
    if second_hero not in all_heroes:
        await update.message.reply_text("⚠️ Будь ласка, оберіть героя з меню.")
        return States.COMPARISON_SECOND_HERO

    await update.message.reply_text(f"Порівняння {first_hero} та {second_hero} буде реалізовано пізніше.")
    reply_markup = get_characters_menu_keyboard()
    await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
    return States.CHARACTERS_MENU

async def handle_selecting_counter_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()

    all_heroes = [hero for heroes in HEROES_BY_CLASS.values() for hero in heroes]
    if hero_name not in all_heroes:
        await update.message.reply_text("⚠️ Будь ласка, оберіть героя з меню.")
        return States.SELECTING_COUNTER_HERO

    await update.message.reply_text(f"Контр-герої для {hero_name} будуть реалізовані пізніше.")
    reply_markup = get_characters_menu_keyboard()
    await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
    return States.CHARACTERS_MENU

async def handle_hero_functions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    hero_name = context.user_data.get('selected_hero')

    if user_input == "🔙 Назад":
        return await handle_selecting_hero(update, context)

    if user_input == "ℹ️ Загальна інформація":
        hero_info = await get_hero_info(hero_name)
        await update.message.reply_text(hero_info, parse_mode='HTML')
    else:
        await update.message.reply_text(
            f"Ви обрали опцію '{user_input}' для героя {hero_name}. Ця функція буде реалізована пізніше."
        )
    
    return States.HERO_FUNCTIONS_MENU

async def get_hero_info(hero_name: str) -> str:
    """Функція для отримання детальної інформації про героя."""
    # Пошук героя у файлі fighter.json
    hero_info = next((hero for hero in fighter_data['heroes'] if hero['name'] == hero_name), None)
    if hero_info:
        details = (
            f"🔸 <b>{hero_info['name']}</b>\n"
            f"🔹 Клас: {hero_info['class']}\n"
            f"🔹 Тип атаки: {hero_info['attack_type']}\n"
            f"🔹 Додаткові ефекти: {hero_info['additional_effects']}\n\n"
            f"📊 <b>Основні характеристики:</b>\n"
            f"Здоров'я: {hero_info['base_stats']['health']}\n"
            f"Атака: {hero_info['base_stats']['physical_attack']}\n"
            f"Фізичний захист: {hero_info['base_stats']['physical_defense']}\n"
            f"Магічний захист: {hero_info['base_stats']['magic_defense']}\n"
            f"Швидкість руху: {hero_info['base_stats']['movement_speed']}\n\n"
            f"🛠️ <b>Рекомендовані предмети:</b>\n" + ", ".join(hero_info['recommended_items']) + "\n\n"
            f"🧬 <b>Навички:</b>\n"
        )
        skills = hero_info.get('skills', {})
        if 'passive' in skills:
            details += f"🔸 <b>Пасивна:</b> {skills['passive']['name']} - {skills['passive']['description']}\n"
        if 'skill1' in skills:
            details += f"🔹 <b>Навичка 1:</b> {skills['skill1']['name']} - {skills['skill1']['description']}\n"
            details += f"    Перезарядка: {skills['skill1'].get('cooldown', 'N/A')}\n"
            details += f"    Витрати мани: {skills['skill1'].get('mana_cost', 'N/A')}\n"
        if 'skill2' in skills:
            details += f"🔹 <b>Навичка 2:</b> {skills['skill2']['name']} - {skills['skill2']['description']}\n"
            details += f"    Перезарядка: {skills['skill2'].get('cooldown', 'N/A')}\n"
            details += f"    Витрати мани: {skills['skill2'].get('mana_cost', 'N/A')}\n"
        if 'ultimate' in skills:
            details += f"💥 <b>Ультимативна:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
            details += f"    Перезарядка: {skills['ultimate'].get('cooldown', 'N/A')}\n"
            details += f"    Витрати мани: {skills['ultimate'].get('mana_cost', 'N/A')}\n"
        return details
    return "Інформація про героя недоступна."

async def show_fighter_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not HEROES_BY_CLASS.get('Борець'):
        await update.message.reply_text("⚠️ Список бійців порожній.")
        return States.CHARACTERS_MENU

    buttons = []
    row = []
    for idx, fighter in enumerate(HEROES_BY_CLASS['Борець'], 1):
        row.append(KeyboardButton(fighter))
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Оберіть бійця:", reply_markup=reply_markup)
    return States.SELECTING_HERO

def format_fighter_info(hero):
    info = f"<b>{hero['name']}</b>\n\n"
    info += f"Клас: {hero['class']}\n"
    info += f"Атака: {hero['attack_type']}\n"
    info += f"Додаткові ефекти: {hero['additional_effects']}\n\n"
    info += "<b>Рекомендовані предмети:</b>\n" + ", ".join(hero['recommended_items']) + "\n\n"
    info += "<b>Базові характеристики:</b>\n"
    for stat, value in hero['base_stats'].items():
        stat_formatted = stat.capitalize().replace('_', ' ')
        info += f"  - {stat_formatted}: {value}\n"
    info += "\n<b>Навички:</b>\n"
    skills = hero.get('skills', {})
    if 'passive' in skills:
        info += f"🔸 <b>Пасивна:</b> {skills['passive']['name']} - {skills['passive']['description']}\n"
    if 'skill1' in skills:
        info += f"🔹 <b>Навичка 1:</b> {skills['skill1']['name']} - {skills['skill1']['description']}\n"
        info += f"    Перезарядка: {skills['skill1'].get('cooldown', 'N/A')}\n"
        info += f"    Витрати мани: {skills['skill1'].get('mana_cost', 'N/A')}\n"
    if 'skill2' in skills:
        info += f"🔹 <b>Навичка 2:</b> {skills['skill2']['name']} - {skills['skill2']['description']}\n"
        info += f"    Перезарядка: {skills['skill2'].get('cooldown', 'N/A')}\n"
        info += f"    Витрати мани: {skills['skill2'].get('mana_cost', 'N/A')}\n"
    if 'ultimate' in skills:
        info += f"💥 <b>Ультимативна:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
        info += f"    Перезарядка: {skills['ultimate'].get('cooldown', 'N/A')}\n"
        info += f"    Витрати мани: {skills['ultimate'].get('mana_cost', 'N/A')}\n"
    return info

async def list_all_heroes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    all_heroes = []
    for heroes in HEROES_BY_CLASS.values():
        all_heroes.extend(heroes)
    buttons = []
    row = []
    for idx, hero in enumerate(all_heroes, 1):
        row.append(KeyboardButton(hero))
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Оберіть героя:", reply_markup=reply_markup)
