# handlers/search.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def handle_search_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [KeyboardButton("🔍 Пошук героїв та гайдів"), KeyboardButton("🎙️ Голосовий пошук")],
        [KeyboardButton("📝 Історія пошуку"), KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
    return States.SEARCH_PERFORMING

async def handle_search_performing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()

    if user_input == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    elif user_input == "🔍 Пошук героїв та гайдів":
        await update.message.reply_text("🔍 Введіть ваш запит для пошуку:")
        return States.SEARCH_HERO_GUIDES
    elif user_input == "🎙️ Голосовий пошук":
        await update.message.reply_text("🎙️ Голосовий пошук наразі не підтримується.")
        return States.SEARCH_PERFORMING
    elif user_input == "📝 Історія пошуку":
        await show_search_history(update, context)
        return States.SEARCH_PERFORMING
    else:
        query = user_input
        return await perform_search(query, update, context)

async def perform_search(query: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    heroes_data = context.bot_data.get('heroes_data', {})
    matching_heroes = [hero_name for hero_name in heroes_data if query.lower() in hero_name.lower()]
    if matching_heroes:
        buttons = []
        row = []
        for idx, hero_name in enumerate(matching_heroes, 1):
            row.append(KeyboardButton(hero_name))
            if idx % 3 == 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([KeyboardButton("🔙 Назад")])
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(f"🔍 Результати пошуку для '{query}':", reply_markup=reply_markup)
        return States.SEARCH_HERO_GUIDES
    else:
        await update.message.reply_text(f"❌ Героїв не знайдено за запитом '{query}'.")
        return States.SEARCH_PERFORMING

async def handle_search_hero_guides(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_hero = update.message.text.strip()
    if selected_hero == "🔙 Назад":
        return await handle_search_menu(update, context)

    heroes_data = context.bot_data.get('heroes_data', {})
    if selected_hero in heroes_data:
        hero_info = heroes_data[selected_hero]
        details = format_hero_info(hero_info)
        await update.message.reply_text(details, parse_mode='HTML')
        return States.SEARCH_PERFORMING
    else:
        await update.message.reply_text("⚠️ Вибраного героя не знайдено.")
        return States.SEARCH_PERFORMING

async def show_search_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    history = context.user_data.get('search_history', [])
    if history:
        history_text = "📝 **Історія пошуку:**\n\n" + "\n".join([f"{idx+1}. {query}" for idx, query in enumerate(history)])
    else:
        history_text = "📝 **Історія пошуку порожня.**"
    await update.message.reply_text(history_text, parse_mode='Markdown')
    return States.SEARCH_PERFORMING

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
        if 'skill2' in skills:
            info += f"🔹 <b>Навичка 2:</b> {skills['skill2']['name']} - {skills['skill2']['description']}\n"
            info += f"    Перезарядка: {skills['skill2'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['skill2'].get('mana_cost', 'N/A')}\n"
        if 'ultimate' in skills:
            info += f"💥 <b>Ультимативна:</b> {skills['ultimate']['name']} - {skills['ultimate']['description']}\n"
            info += f"    Перезарядка: {skills['ultimate'].get('cooldown', 'N/A')}\n"
            info += f"    Витрати мани: {skills['ultimate'].get('mana_cost', 'N/A')}\n"

    return info
