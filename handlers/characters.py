# handlers/characters.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging
import os
import openai
import json
from utils.data_loader import load_heroes_data

logger = logging.getLogger(__name__)

# Ініціалізація OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Завантаження базових даних про героїв
heroes_data = load_heroes_data()

def get_hero_classes_keyboard(context):
    heroes_by_class = {}
    for hero, info in heroes_data.items():
        cls = info['class']
        if cls not in heroes_by_class:
            heroes_by_class[cls] = []
        heroes_by_class[cls].append(hero)
    
    buttons = []
    for cls, heroes in heroes_by_class.items():
        buttons.append([KeyboardButton(cls)])
    buttons.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_heroes_keyboard(context):
    selected_class = context.user_data.get('selected_class')
    heroes = []
    for hero, info in heroes_data.items():
        if info['class'] == selected_class:
            heroes.append(hero)
    
    buttons = []
    for i in range(0, len(heroes), 3):
        buttons.append([KeyboardButton(hero) for hero in heroes[i:i+3]])
    buttons.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    
    if selected_class == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU
    
    if selected_class not in [info['class'] for info in heroes_data.values()]:
        reply_markup = get_hero_classes_keyboard(context)
        await update.message.reply_text("Будь ласка, оберіть клас героя з меню:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS
    
    context.user_data['selected_class'] = selected_class
    heroes = [hero for hero, info in heroes_data.items() if info['class'] == selected_class]
    
    logger.info(f"Heroes in class {selected_class}: {heroes}")
    
    if not heroes:
        await update.message.reply_text(f"⚠️ Немає доступних героїв у класі {selected_class}.")
        return States.SELECTING_HERO_CLASS
    
    reply_markup = get_heroes_keyboard(context)
    await update.message.reply_text(f"Виберіть героя з класу {selected_class}:", reply_markup=reply_markup)
    return States.SELECTING_HERO

async def handle_selecting_hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        hero_name = update.message.text.strip()
        if hero_name == "🔙 Назад":
            reply_markup = get_hero_classes_keyboard(context)
            await update.message.reply_text("Оберіть клас героя:", reply_markup=reply_markup)
            return States.SELECTING_HERO_CLASS
    
        selected_class = context.user_data.get('selected_class')
        heroes = [hero for hero, info in heroes_data.items() if info['class'] == selected_class]
    
        if hero_name not in heroes:
            await update.message.reply_text("⚠️ Будь ласка, виберіть героя з меню.")
            return States.SELECTING_HERO
    
        context.user_data['selected_hero'] = hero_name
    
        buttons = [
            [KeyboardButton("ℹ️ Загальна інформація"), KeyboardButton("🛠️ Побудови")],
            [KeyboardButton("📖 Гайди"), KeyboardButton("🗺️ Стратегії")],
            [KeyboardButton("🎯 Контр-Піки"), KeyboardButton("⚔️ Порівняння")],
            [KeyboardButton("🔙 Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(f"Ви вибрали {hero_name}. Виберіть опцію:", reply_markup=reply_markup)
        return States.HERO_FUNCTIONS_MENU
    except Exception as e:
        logger.error(f"Помилка в handle_selecting_hero: {e}")
        await update.message.reply_text("Виникла помилка. Спробуйте ще раз.")
        return States.SELECTING_HERO

async def handle_hero_functions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_input = update.message.text.strip()
        hero_name = context.user_data.get('selected_hero')
        hero_class = context.user_data.get('selected_class')
    
        if user_input == "🔙 Назад":
            reply_markup = get_heroes_keyboard(context)
            await update.message.reply_text(f"Виберіть героя з класу {hero_class}:", reply_markup=reply_markup)
            return States.SELECTING_HERO
    
        if user_input == "ℹ️ Загальна інформація":
            hero_info = await handle_gpt_query(hero_name, context)
            if hero_info:
                await update.message.reply_text(hero_info, parse_mode='HTML')
            else:
                await update.message.reply_text("⚠️ Виникла помилка при отриманні інформації про героя.")
        else:
            # Реалізація інших функцій може бути додана тут
            await update.message.reply_text(f"Ви вибрали '{user_input}' для героя {hero_name}. Ця функція буде реалізована пізніше.")
    
        return States.HERO_FUNCTIONS_MENU
    except Exception as e:
        logger.error(f"Помилка в handle_hero_functions_menu: {e}")
        await update.message.reply_text("Виникла помилка. Спробуйте ще раз.")
        return States.HERO_FUNCTIONS_MENU

async def handle_gpt_query(hero_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Функція для отримання детальної інформації про героя через AI API."""
    try:
        # Отримання базової інформації про героя
        hero_info = heroes_data.get(hero_name)
        if not hero_info:
            return "⚠️ Не вдалося знайти інформацію про цього героя."
    
        # Створення системного промпту
        system_prompt = """
Ти — інформативний і дружній помічник Telegram-бота для надання інформації про героїв гри Mobile Legends: Bang Bang. Відповідай лаконічно, використовуючи українську мову. Використовуй надану базову інформацію про героя для створення повного опису.
        """
    
        # Створення промпту на основі базової інформації
        base_info = f"""
Ім'я героя: {hero_name}
Клас: {hero_info['class']}
Роль: {hero_info['role']}
Швидкість: {hero_info['speed']}
Здоров'я (HP): {hero_info['hp']}
Мана (MP): {hero_info['mp']}
Фізичний захист: {hero_info['physical_defense']}
Магічний захист: {hero_info['magical_defense']}
Швидкість атаки: {hero_info['attack_speed']}

Навички:
"""
        for idx, skill in enumerate(hero_info['skills'], 1):
            base_info += f"{idx}. {skill['name']}\n   Опис: {skill['description']}\n   Час перезарядки: {skill['cooldown']}\n   Витрати мани: {skill['mana_cost']}\n\n"
    
        strategies = hero_info['strategies']
        recommendations = hero_info['recommendations']
        drafts = hero_info['drafts']
    
        base_info += f"""
Стратегії:
• Агресивна стратегія: {strategies['aggressive_strategy']}
• Захисна стратегія: {strategies['defensive_strategy']}

Рекомендації щодо гри:
• Ранній етап: {recommendations['early_game']}
• Середній етап: {recommendations['mid_game']}
• Пізня гра: {recommendations['late_game']}

Драфти:
• Ідеальні союзники: {drafts['ideal_allies']}
• Кого краще уникати: {drafts['avoid_enemies']}
• Сильні драфти: {drafts['strong_drafts']}
        """
    
        # Формування повного промпту
        user_prompt = f"""
На основі наступної базової інформації, створіть повний опис героя Mobile Legends: Bang Bang. Використовуйте надані дані та додайте свої рекомендації щодо стратегії та гри.

{base_info}
        """
    
        # Виклик OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
        )
    
        ai_text = response.choices[0].message['content'].strip()
    
        # Форматуємо відповідь для Telegram
        formatted_text = format_ai_response(ai_text)
        return formatted_text
    except Exception as e:
        logger.error(f"Помилка при зверненні до OpenAI API: {e}")
        return "⚠️ Сталася невідома помилка при обробці вашого запиту."

def format_ai_response(ai_text: str) -> str:
    """Форматуємо відповідь від AI для відправки користувачу."""
    # Ви можете додати додаткове форматування, наприклад, HTML
    formatted_text = ai_text.replace('\n', '<br>')
    return formatted_text
                                     
