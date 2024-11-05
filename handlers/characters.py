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

def get_hero_classes_keyboard(context):
    heroes_by_class = context.bot_data.get('heroes_by_class', {})
    buttons = []
    row = []
    for idx, class_name in enumerate(heroes_by_class.keys(), 1):
        row.append(KeyboardButton(class_name))
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_heroes_keyboard(context):
    selected_class = context.user_data.get('selected_class')
    heroes = context.bot_data.get('heroes_by_class', {}).get(selected_class, [])
    buttons = []
    row = []
    for idx, hero_name in enumerate(heroes, 1):
        row.append(KeyboardButton(hero_name))
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    heroes_by_class = context.bot_data.get('heroes_by_class', {})

    if selected_class == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    # Якщо вибраний клас не є дійсним, показуємо список класів
    if selected_class not in heroes_by_class:
        reply_markup = get_hero_classes_keyboard(context)
        await update.message.reply_text("Будь ласка, оберіть клас героя з меню:", reply_markup=reply_markup)
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = heroes_by_class[selected_class]

    # Логування списку героїв
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
        heroes = context.bot_data.get('heroes_by_class', {}).get(selected_class, [])

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
            hero_info = await get_hero_info(hero_name, context)
            if hero_info:
                await update.message.reply_text(hero_info, parse_mode='HTML', disable_web_page_preview=True)
            else:
                await update.message.reply_text("⚠️ Виникла помилка при отриманні інформації про героя.")
        else:
            # Можна додати реалізацію інших функцій у майбутньому
            await update.message.reply_text(f"Ви вибрали '{user_input}' для героя {hero_name}. Ця функція буде реалізована пізніше.")

        return States.HERO_FUNCTIONS_MENU
    except Exception as e:
        logger.error(f"Помилка в handle_hero_functions_menu: {e}")
        await update.message.reply_text("Виникла помилка. Спробуйте ще раз.")
        return States.HERO_FUNCTIONS_MENU

async def get_hero_info(hero_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Функція для отримання детальної інформації про героя через AI API."""
    try:
        # Отримання базової інформації про героя
        heroes_data = context.bot_data.get('heroes_data', {})
        hero_info = heroes_data.get(hero_name)

        if not hero_info:
            return "⚠️ Не вдалося знайти інформацію про цього героя."

        # Створення системного промпту
        system_prompt = """
Ти — інформативний і дружній помічник Telegram-бота для надання інформації про героїв гри Mobile Legends: Bang Bang. Відповідай лаконічно, використовуючи українську мову. Використовуй надану базову інформацію про героя для створення повного опису.
        """

        # Створення промпту на основі базової інформації
        base_info = f"""
Ім'я героя: {hero_info.get('name', 'Невідомо')}
Клас: {hero_info.get('class', 'N/A')}
Роль: {hero_info.get('role', 'N/A')}
Швидкість: {hero_info.get('speed', 'N/A')}
Здоров'я (HP): {hero_info.get('hp', 'N/A')}
Мана (MP): {hero_info.get('mp', 'N/A')}
Фізичний захист: {hero_info.get('physical_defense', 'N/A')}
Магічний захист: {hero_info.get('magical_defense', 'N/A')}
Швидкість атаки: {hero_info.get('attack_speed', 'N/A')}

Навички:
"""
        skills = hero_info.get('skills', {})
        for skill_type in ['passive', 'skill1', 'skill2', 'ultimate']:
            skill = skills.get(skill_type)
            if skill:
                info = f"{skill_type.capitalize()}: {skill.get('name', 'N/A')}\nОпис: {skill.get('description', 'N/A')}\nЧас перезарядки: {skill.get('cooldown', 'N/A')}\nВитрати мани: {skill.get('mana_cost', 'N/A')}\n\n"
                base_info += info

        strategies = hero_info.get('strategies', {})
        recommendations = hero_info.get('recommendations', {})
        drafts = hero_info.get('drafts', {})

        base_info += f"""
Стратегії:
• Агресивна стратегія: {strategies.get('aggressive', 'N/A')}
• Захисна стратегія: {strategies.get('defensive', 'N/A')}
• Мікрогра: {strategies.get('micro', 'N/A')}

Рекомендації щодо гри:
• Ранній етап: {recommendations.get('early_game', 'N/A')}
• Середній етап: {recommendations.get('mid_game', 'N/A')}
• Пізня гра: {recommendations.get('late_game', 'N/A')}

Драфти:
• Ідеальні союзники: {drafts.get('ideal_allies', 'N/A')}
• Кого краще уникати: {drafts.get('avoid_enemies', 'N/A')}
• Сильні драфти: {drafts.get('strong_drafts', 'N/A')}
        """

        # Формування повного промпту
        user_prompt = f"""
На основі наступної базової інформації, створіть повний опис героя Mobile Legends: Bang Bang. Використовуйте надані дані та додайте свої рекомендації щодо стратегії та гри.

{base_info}
        """

        # Перевірка наявності кешованої відповіді
        cache = context.bot_data.get('ai_responses', {})
        cache_key = f"{hero_name}_{hero_class}"
        if cache_key in cache:
            logger.info(f"Отримано дані з кешу для {hero_name} ({hero_class})")
            return cache[cache_key]

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

        # Зберігаємо в кеш
        cache[cache_key] = formatted_text
        context.bot_data['ai_responses'] = cache

        logger.info(f"Відповідь від AI успішно отримана для героя: {hero_name}")

        return formatted_text
    except Exception as e:
        logger.error(f"Помилка при зверненні до OpenAI API: {e}")
        return "⚠️ Сталася невідома помилка при обробці вашого запиту."

def format_ai_response(ai_text: str) -> str:
    """Форматуємо відповідь від AI для відправки користувачу."""
    # Додайте додаткове форматування, наприклад, HTML
    formatted_text = ai_text.replace('\n', '<br>')
    return formatted_text
                           
