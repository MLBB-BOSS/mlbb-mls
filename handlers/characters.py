# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_all_heroes
import logging

logger = logging.getLogger(__name__)

# Завантаження всіх героїв
HEROES_BY_CLASS = load_all_heroes()

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    if selected_class == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    if selected_class not in HEROES_BY_CLASS:
        # Відображаємо клавіатуру з класами знову
        buttons = []
        classes = list(HEROES_BY_CLASS.keys())
        row = []
        for idx, class_name in enumerate(classes, 1):
            row.append(KeyboardButton(class_name))
            if idx % 3 == 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([KeyboardButton("🔙 Назад")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("⚠️ Будь ласка, оберіть клас з меню.", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = HEROES_BY_CLASS[selected_class]
    buttons = []
    row = []
    for idx, hero in enumerate(heroes, 1):
        row.append(KeyboardButton(hero['name']))
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
        # Повертаємося до вибору класу героя
        return await handle_selecting_hero_class(update, context)

    selected_class = context.user_data.get('selected_class')
    if selected_class is None or not any(hero['name'] == hero_name for hero in HEROES_BY_CLASS.get(selected_class, [])):
        # Відображаємо список героїв знову
        heroes = HEROES_BY_CLASS[selected_class]
        buttons = []
        row = []
        for idx, hero in enumerate(heroes, 1):
            row.append(KeyboardButton(hero['name']))
            if idx % 3 == 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([KeyboardButton("🔙 Назад")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("⚠️ Будь ласка, оберіть героя з меню.", reply_markup=reply_markup)
        return States.SELECTING_HERO

    context.user_data['selected_hero'] = hero_name

    buttons = [
        [KeyboardButton("ℹ️ Загальна інформація"), KeyboardButton("🛠️ Білди")],
        [KeyboardButton("📖 Гайди"), KeyboardButton("🗺️ Стратегії")],
        [KeyboardButton("🎯 Контрпіки"), KeyboardButton("⚔️ Порівняння")],
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
    for class_name, heroes in HEROES_BY_CLASS.items():
        hero_info = next((hero for hero in heroes if hero['name'].lower() == hero_name.lower()), None)
        if hero_info:
            details = format_hero_info(hero_info)
            return details
    return "Інформація про героя недоступна."

def format_hero_info(hero):
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
    if 'skill3' in skills:
        info += f"🔹 <b>Навичка 3:</b> {skills['skill3']['name']} - {skills['skill3']['description']}\n"
        info += f"    Перезарядка: {skills['skill3'].get('cooldown', 'N/A')}\n"
        info += f"    Витрати мани: {skills['skill3'].get('mana_cost', 'N/A')}\n"
    if 'ultimate' in skills:
        info += f"💥 <b>Ультимативна:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
        info += f"    Перезарядка: {skills['ultimate'].get('cooldown', 'N/A')}\n"
        info += f"    Витрати мани: {skills['ultimate'].get('mana_cost', 'N/A')}\n"
    return info
