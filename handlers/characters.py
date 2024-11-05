# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_all_heroes
import logging

logger = logging.getLogger(__name__)

# Завантаження всіх героїв з файлів
HEROES_BY_CLASS = load_all_heroes()

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    if selected_class == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    if selected_class not in HEROES_BY_CLASS:
        await update.message.reply_text("⚠️ Будь ласка, виберіть клас з меню.")
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = HEROES_BY_CLASS[selected_class]
    
    # Логування списку героїв
    hero_names = [hero['name'] for hero in heroes]
    logger.info(f"Heroes in class {selected_class}: {hero_names}")
    
    if not heroes:
        await update.message.reply_text(f"⚠️ Немає доступних героїв у класі {selected_class}.")
        return States.SELECTING_HERO_CLASS

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
    await update.message.reply_text(f"Виберіть героя з класу {selected_class}:", reply_markup=reply_markup)
    return States.SELECTING_HERO

async def handle_selecting_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    if hero_name == "🔙 Назад":
        # Повернення до вибору класу героя
        return await handle_selecting_hero_class(update, context)

    selected_class = context.user_data.get('selected_class')
    if selected_class is None or not any(hero['name'] == hero_name for hero in HEROES_BY_CLASS.get(selected_class, [])):
        # Показати список героїв знову
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
        await update.message.reply_text("⚠️ Будь ласка, виберіть героя з меню.", reply_markup=reply_markup)
        return States.SELECTING_HERO

    context.user_data['selected_hero'] = hero_name

    buttons = [
        [KeyboardButton("ℹ️ Загальна інформація"), KeyboardButton("🛠️ Побудови")],
        [KeyboardButton("📖 Гіди"), KeyboardButton("🗺️ Стратегії")],
        [KeyboardButton("🎯 Контр-Піки"), KeyboardButton("⚔️ Порівняння")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Ви вибрали {hero_name}. Виберіть опцію:", reply_markup=reply_markup)
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
        # Можна додати реалізацію інших функцій у майбутньому
        translated_options = {
            "🛠️ Побудови": "Builds",
            "📖 Гіди": "Guides",
            "🗺️ Стратегії": "Strategies",
            "🎯 Контр-Піки": "Counter Picks",
            "⚔️ Порівняння": "Compare"
        }
        selected_option = translated_options.get(user_input, user_input)
        await update.message.reply_text(
            f"Ви вибрали '{selected_option}' для героя {hero_name}. Ця функція буде реалізована пізніше."
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
    info += f"Тип атаки: {hero.get('attack_type', 'N/A')}\n"
    info += f"Додаткові ефекти: {hero.get('additional_effects', 'N/A')}\n\n"
    
    if "recommended_items" in hero and hero["recommended_items"]:
        info += "<b>Рекомендовані предмети:</b>\n" + ", ".join(hero['recommended_items']) + "\n\n"
    
    if "base_stats" in hero and hero["base_stats"]:
        info += "<b>Базові статистики:</b>\n"
        for stat, value in hero['base_stats'].items():
            stat_formatted = stat.capitalize().replace('_', ' ')
            info += f"  - {stat_formatted}: {value}\n"
        info += "\n"
    
    if "skills" in hero and hero["skills"]:
        info += "<b>Навички:</b>\n"
        skills = hero['skills']
        if 'passive' in skills:
            info += f"🔸 <b>Пасивна:</b> {skills['passive']['name']} - {skills['passive']['description']}\n"
        if 'skill1' in skills:
            info += f"🔹 <b>Навичка 1:</b> {skills['skill1']['name']} - {skills['skill1']['description']}\n"
            info += f"    Перезарядка: {skills['skill1'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['skill1'].get('mana_cost', 'N/A')}\n"
            if 'energy_cost' in skills['skill1'] and skills['skill1']['energy_cost'] is not None:
                info += f"    Витрати енергії: {skills['skill1'].get('energy_cost')}\n"
        if 'skill2' in skills:
            info += f"🔹 <b>Навичка 2:</b> {skills['skill2']['name']} - {skills['skill2']['description']}\n"
            info += f"    Перезарядка: {skills['skill2'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['skill2'].get('mana_cost', 'N/A')}\n"
            if 'energy_cost' in skills['skill2'] and skills['skill2']['energy_cost'] is not None:
                info += f"    Витрати енергії: {skills['skill2'].get('energy_cost')}\n"
        if 'skill3' in skills:
            info += f"🔹 <b>Навичка 3:</b> {skills['skill3']['name']} - {skills['skill3']['description']}\n"
            info += f"    Перезарядка: {skills['skill3'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['skill3'].get('mana_cost', 'N/A')}\n"
            if 'energy_cost' in skills['skill3'] and skills['skill3']['energy_cost'] is not None:
                info += f"    Витрати енергії: {skills['skill3'].get('energy_cost')}\n"
        if 'ultimate' in skills:
            info += f"💥 <b>Ультимативна:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
            info += f"    Перезарядка: {skills['ultimate'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['ultimate'].get('mana_cost', 'N/A')}\n"
            if 'energy_cost' in skills['ultimate'] and skills['ultimate']['energy_cost'] is not None:
                info += f"    Витрати енергії: {skills['ultimate'].get('energy_cost')}\n"
    return info
