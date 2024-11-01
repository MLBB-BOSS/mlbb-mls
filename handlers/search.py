# handlers/search.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States
from utils.data_loader import load_json_data
import logging

logger = logging.getLogger(__name__)

async def handle_search_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger.info(f"Вибір в Пошуку: {user_input}")
    
    if user_input == "🔍 Пошук героїв та гайдів":
        await perform_search(update, context)
        return States.SEARCH_PERFORMING
    elif user_input == "🎙️ Голосовий пошук":
        await perform_voice_search(update, context)
        return States.SEARCH_PERFORMING
    elif user_input == "📝 Історія пошуку":
        await show_search_history(update, context)
        return States.SEARCH_PERFORMING
    elif user_input == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.SEARCH_PERFORMING

async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🔍 Введіть ваш запит для пошуку:")
    return States.SEARCH_PERFORMING

async def perform_voice_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🎙️ Голосовий пошук наразі не підтримується.")
    return States.SEARCH_PERFORMING

async def show_search_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    history = context.user_data.get('search_history', [])
    if history:
        history_text = "📝 **Історія пошуку:**\n\n" + "\n".join([f"{idx+1}. {query}" for idx, query in enumerate(history)])
    else:
        history_text = "📝 **Історія пошуку порожня.**"
    await update.message.reply_text(history_text, parse_mode='Markdown')
    return States.SEARCH_PERFORMING

async def handle_search_performing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.message.text.strip()
    if query:
        # Зберігаємо запит у історію пошуку
        if 'search_history' not in context.user_data:
            context.user_data['search_history'] = []
        context.user_data['search_history'].append(query)
        
        # Виконуємо пошук героїв
        matching_heroes = [
            hero["name"] for hero in load_json_data('data/characters.json').get('heroes', [])
            if query.lower() in hero["name"].lower()
        ]
        
        if matching_heroes:
            buttons = []
            for i in range(0, len(matching_heroes), 4):
                row = matching_heroes[i:i + 4]
                buttons.append([KeyboardButton(hero) for hero in row])
            buttons.append([KeyboardButton("🔙 Назад")])
            reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            await update.message.reply_text(f"🔍 **Результати пошуку для '{query}':**", parse_mode='Markdown', reply_markup=reply_markup)
            return States.SEARCH_HERO_GUIDES
        else:
            await update.message.reply_text(f"🔍 Немає героїв або гайдів, що відповідають '{query}'.")
            from handlers.start_handler import start
            await start(update, context)
            return States.MAIN_MENU
    else:
        await update.message.reply_text("Будь ласка, введіть коректний запит для пошуку.")
        return States.SEARCH_PERFORMING

async def handle_search_hero_guides(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_hero = update.message.text.strip()
    heroes = load_json_data('data/characters.json').get('heroes', [])
    hero_info = next((hero for hero in heroes if hero['name'] == selected_hero), None)
    if hero_info:
        hero_details = (
            f"📖 **Деталі про героя {selected_hero}:**\n\n"
            f"<b>Клас:</b> {hero_info.get('class', 'Невідомо')}\n"
            f"<b>Роль:</b> {hero_info.get('role', 'Невідомо')}\n"
            f"<b>HP:</b> {hero_info.get('hp', 'Невідомо')}\n"
            f"<b>Атака:</b> {hero_info.get('attack', 'Невідомо')}\n"
            f"<b>Захист:</b> {hero_info.get('defense', 'Невідомо')}\n\n"
            f"🔗 Детальніше: {hero_info.get('details_link', 'Немає посилання')}"
        )
        await update.message.reply_text(hero_details, parse_mode='HTML', disable_web_page_preview=True)
        # Повернення до пошуку
        buttons = [
            [KeyboardButton("🔍 Пошук героїв та гайдів"), KeyboardButton("🎙️ Голосовий пошук")],
            [KeyboardButton("📝 Історія пошуку"), KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
        return States.SEARCH_PERFORMING
    elif selected_hero == "🔙 Назад":
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Вибрана опція не відповідає жодному герою.")
        from handlers.start_handler import start
        await start(update, context)
        return States.MAIN_MENU
