# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import asyncio
import logging

logger = logging.getLogger(__name__)

# Словник з героями за класами
HEROES_BY_CLASS = {
    'Танк': [
        'Akai', 'Barats', 'Baxia', 'Belerick', 'Franco',
        'Gatotkaca', 'Gloo', 'Grock', 'Hylos', 'Johnson',
        'Khufra', 'Lolita', 'Minotaur', 'Tigreal'
    ],
    'Маг': [
        'Alice', 'Esmeralda', 'Eudora', 'Gord', 'Harley',
        'Kimmy', 'Lunox', 'Nana', 'Valir', 'Xavier', 'Zhuxin'
    ],
    'Стрілець': [
        'Beatrix', 'Brody', 'Bruno', 'Claude', 'Clint',
        'Dyrroth', 'Granger', 'Hanabi', 'Hilda', 'Karrie',
        'Layla', 'Lesley', 'Martis', 'Miya', 'Wanwan'
    ],
    'Підтримка': [
        'Angela', 'Carmilla', 'Chip', 'Diggie', 'Estes',
        'Floryn', 'Kaja', 'Nana', 'Rafaela'
    ],
    'Борець': [
        'Aldous', 'Alpha', 'Alucard', 'Argus', 'Arlott', 'Aulus',
        'Badang', 'Balmond', 'Bane', 'Chou', 'Freya', 'Guinivere',
        'Jawhead', 'Khaleed', 'LapuLapu', 'Leomord', 'Masha',
        'Minsitthar', 'Paquito', 'Phoveus', 'Roger', 'Ruby', 'Silvanna',
        'Sun', 'Terizla', 'Thamuz', 'X.Borg', 'Yin', 'YuZhong', 'Zilong'
    ],
    'Убивця': [
        'Benedetta', 'Fanny', 'Gusion', 'Hanzo', 'Helcurt',
        'Julian', 'Karina', 'Lancelot', 'Natalia', 'Saber', 'Selena'
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

    logger.debug(f"Вибір у Героях: {user_input}")

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

    # Відображаємо опції для обраного героя
    buttons = [
        [KeyboardButton("ℹ️ Загальна інформація"), KeyboardButton("🎯 Контрпіки")],
        [KeyboardButton("📖 Гайди"), KeyboardButton("🗺️ Стратегії")],
        [KeyboardButton("⚔️ Порівняння"), KeyboardButton("🛠️ Білди")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Ви обрали героя {hero_name}. Оберіть опцію:", reply_markup=reply_markup)
    return States.HERO_FUNCTIONS_MENU

async def handle_hero_functions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    hero_name = context.user_data.get('selected_hero')

    if user_input == "🔙 Назад":
        return await handle_selecting_hero(update, context)

    # Оскільки даних поки немає, просто повідомляємо про вибір
    await update.message.reply_text(f"Ви обрали опцію '{user_input}' для героя {hero_name}. Ця функція буде реалізована пізніше.")
    return States.HERO_FUNCTIONS_MENU

async def handle_comparison_first_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    first_hero = update.message.text.strip()
    context.user_data['first_hero'] = first_hero
    await update.message.reply_text(f"Ви обрали {first_hero}. Тепер оберіть другого героя для порівняння:")
    await list_all_heroes(update, context)
    return States.COMPARISON_SECOND_HERO

async def handle_comparison_second_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    second_hero = update.message.text.strip()
    first_hero = context.user_data.get('first_hero')
    # Тут ви можете реалізувати функцію порівняння
    await update.message.reply_text(f"Порівняння {first_hero} та {second_hero} буде реалізовано пізніше.")
    reply_markup = get_characters_menu_keyboard()
    await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
    return States.CHARACTERS_MENU

async def handle_selecting_counter_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    # Тут ви можете реалізувати функцію відображення контр-героїв
    await update.message.reply_text(f"Контр-герої для {hero_name} будуть реалізовані пізніше.")
    reply_markup = get_characters_menu_keyboard()
    await update.message.reply_text("🦸 Оберіть опцію:", reply_markup=reply_markup)
    return States.CHARACTERS_MENU

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
