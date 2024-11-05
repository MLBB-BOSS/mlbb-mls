# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
from utils.data_loader import load_all_heroes
import logging

logger = logging.getLogger(__name__)

HEROES_BY_CLASS = load_all_heroes()

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    if selected_class == "🔙 Back":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Returning to main menu:", reply_markup=reply_markup)
        return States.MAIN_MENU

    if selected_class not in HEROES_BY_CLASS:
        await update.message.reply_text("⚠️ Please select a class from the menu.")
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = HEROES_BY_CLASS[selected_class]
    
    # Log the list of heroes
    hero_names = [hero['name'] for hero in heroes]
    logger.info(f"Heroes in class {selected_class}: {hero_names}")
    
    if not heroes:
        await update.message.reply_text(f"⚠️ No heroes available in the class {selected_class}.")
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
    buttons.append([KeyboardButton("🔙 Back")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Select a hero from the {selected_class} class:", reply_markup=reply_markup)
    return States.SELECTING_HERO

async def handle_selecting_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hero_name = update.message.text.strip()
    if hero_name == "🔙 Back":
        # Return to hero class selection
        return await handle_selecting_hero_class(update, context)

    selected_class = context.user_data.get('selected_class')
    if selected_class is None or not any(hero['name'] == hero_name for hero in HEROES_BY_CLASS.get(selected_class, [])):
        # Show the hero list again
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
        buttons.append([KeyboardButton("🔙 Back")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("⚠️ Please select a hero from the menu.", reply_markup=reply_markup)
        return States.SELECTING_HERO

    context.user_data['selected_hero'] = hero_name

    buttons = [
        [KeyboardButton("ℹ️ General Info"), KeyboardButton("🛠️ Builds")],
        [KeyboardButton("📖 Guides"), KeyboardButton("🗺️ Strategies")],
        [KeyboardButton("🎯 Counter Picks"), KeyboardButton("⚔️ Compare")],
        [KeyboardButton("🔙 Back")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"You have selected {hero_name}. Choose an option:", reply_markup=reply_markup)
    return States.HERO_FUNCTIONS_MENU

async def handle_hero_functions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()
    hero_name = context.user_data.get('selected_hero')

    if user_input == "🔙 Back":
        return await handle_selecting_hero(update, context)

    if user_input == "ℹ️ General Info":
        hero_info = await get_hero_info(hero_name)
        await update.message.reply_text(hero_info, parse_mode='HTML')
    else:
        await update.message.reply_text(
            f"You selected '{user_input}' for hero {hero_name}. This feature will be implemented later."
        )

    return States.HERO_FUNCTIONS_MENU

async def get_hero_info(hero_name: str) -> str:
    """Function to get detailed information about a hero."""
    for class_name, heroes in HEROES_BY_CLASS.items():
        hero_info = next((hero for hero in heroes if hero['name'].lower() == hero_name.lower()), None)
        if hero_info:
            details = format_hero_info(hero_info)
            return details
    return "Information about the hero is unavailable."

def format_hero_info(hero):
    info = f"<b>{hero['name']}</b>\n\n"
    info += f"Class: {hero['class']}\n"
    info += f"Attack Type: {hero['attack_type']}\n"
    info += f"Additional Effects: {hero['additional_effects']}\n\n"
    info += "<b>Recommended Items:</b>\n" + ", ".join(hero['recommended_items']) + "\n\n"
    info += "<b>Base Stats:</b>\n"
    for stat, value in hero['base_stats'].items():
        stat_formatted = stat.capitalize().replace('_', ' ')
        info += f"  - {stat_formatted}: {value}\n"
    info += "\n<b>Skills:</b>\n"
    skills = hero.get('skills', {})
    if 'passive' in skills:
        info += f"🔸 <b>Passive:</b> {skills['passive']['name']} - {skills['passive']['description']}\n"
    if 'skill1' in skills:
        info += f"🔹 <b>Skill 1:</b> {skills['skill1']['name']} - {skills['skill1']['description']}\n"
        info += f"    Cooldown: {skills['skill1'].get('cooldown', 'N/A')}\n"
        info += f"    Mana Cost: {skills['skill1'].get('mana_cost', 'N/A')}\n"
    if 'skill2' in skills:
        info += f"🔹 <b>Skill 2:</b> {skills['skill2']['name']} - {skills['skill2']['description']}\n"
        info += f"    Cooldown: {skills['skill2'].get('cooldown', 'N/A')}\n"
        info += f"    Mana Cost: {skills['skill2'].get('mana_cost', 'N/A')}\n"
    if 'skill3' in skills:
        info += f"🔹 <b>Skill 3:</b> {skills['skill3']['name']} - {skills['skill3']['description']}\n"
        info += f"    Cooldown: {skills['skill3'].get('cooldown', 'N/A')}\n"
        info += f"    Mana Cost: {skills['skill3'].get('mana_cost', 'N/A')}\n"
    if 'ultimate' in skills:
        info += f"💥 <b>Ultimate:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
        info += f"    Cooldown: {skills['ultimate'].get('cooldown', 'N/A')}\n"
        info += f"    Mana Cost: {skills['ultimate'].get('mana_cost', 'N/A')}\n"
    return info
