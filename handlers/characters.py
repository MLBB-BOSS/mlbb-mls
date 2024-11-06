# handlers/characters.py

import openai 
import logging 
from telegram.ext import ContextTypes 
from utils.formatting import format_ai_response  # Імпорт функції форматування

# Налаштування логування 
logger = logging.getLogger(__name__) 

async def get_hero_info(hero_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:  
    """Функція для отримання детальної інформації про героя через OpenAI API.""" 
    try: 
        # Отримання базової інформації про героя 
        heroes_data = context.bot_data.get('heroes_data', {}) 
        hero_info = heroes_data.get(hero_name) 

        if not hero_info: 
            return "⚠️ Не вдалося знайти інформацію про цього героя." 

        # Отримання класу героя для кешування 
        hero_class = hero_info.get('class', 'Unknown') 

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
            model="gpt-3.5-turbo", 
            messages=[ 
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_prompt} 
            ], 
            max_tokens=1500, 
            temperature=0.7, 
        ) 

        ai_text = response.choices[0].message['content'].strip() 

        # Форматуємо відповідь для Telegram 
        formatted_text = format_ai_response(ai_text)  # Визначена або імпортована функція форматування 

        # Зберігаємо в кеш 
        cache[cache_key] = formatted_text 
        context.bot_data['ai_responses'] = cache 

        logger.info(f"Відповідь від AI успішно отримана для героя: {hero_name}") 

        return formatted_text 

    except Exception as e: 
        logger.error(f"Помилка під час отримання інформації про героя: {e}") 
        return "⚠️ Виникла помилка при обробці запиту. Спробуйте пізніше."
    ```

### 5. Виправлення Структури Репозиторію

Ваш репозиторій має добру структуру, але переконайтеся, що всі модулі містять файл `__init__.py`, щоб Python розпізнавав їх як пакети. Згідно з вашою структурою, це вже зроблено для каталогу `handlers` та `utils`.

### 6. Оновлений Код `main.py`

Переконаємося, що `main.py` правильно імпортує всі необхідні функції та модулі. Також додамо імпорт `handle_gpt_query`, якщо вона використовується.

```python
# main.py

import logging
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from handlers.states import States
from handlers.main_menu import main_menu_handler, unknown_command
from handlers.characters import (
    handle_selecting_hero_class,
    handle_selecting_hero,
    handle_hero_functions_menu
)
from handlers.profile import profile_handler, profile_menu_handler
from handlers.start_handler import start
from utils.data_loader import load_all_heroes, load_heroes_data
from utils.formatting import format_ai_response  # Імпорт функції форматування
from utils.openai_api import handle_gpt_query  # Імпорт функції для роботи з OpenAI
import asyncio
import random

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_trigger_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    message_text = update.message.text.lower()

    TRIGGER_WORDS = ["герой", "персонаж", "геймплей", "mlbb", "mobile legends"]  # Приклад тригерних слів

    if any(trigger in message_text for trigger in TRIGGER_WORDS):
        # Вибір випадкового героя
        heroes_data = context.bot_data.get('heroes_data', {})
        if not heroes_data:
            await update.message.reply_text("⚠️ Інформація про героїв наразі недоступна.")
            return

        hero_name = random.choice(list(heroes_data.keys()))
        # Переконайтеся, що функція handle_gpt_query визначена та імпортована
        gpt_response = await handle_gpt_query(hero_name, context)
        await update.message.reply_text(gpt_response, parse_mode='HTML', disable_web_page_preview=True)

async def main():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if not TELEGRAM_BOT_TOKEN:
        logger.error("Будь ласка, встановіть TELEGRAM_BOT_TOKEN як змінну середовища.")
        return

    if not OPENAI_API_KEY:
        logger.error("Будь ласка, встановіть OPENAI_API_KEY як змінну середовища.")
        return

    # Завантаження даних про героїв
    heroes_by_class = load_all_heroes()
    heroes_data = load_heroes_data()

    # Ініціалізація бота
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додаємо обробник команди /start
    application.add_handler(CommandHandler('start', start))

    # Додаємо ConversationHandler для складних сценаріїв
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)
            ],
            States.SELECTING_HERO_CLASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero_class)
            ],
            States.SELECTING_HERO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selecting_hero)
            ],
            States.HERO_FUNCTIONS_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hero_functions_menu)
            ],
            States.PROFILE_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, profile_menu_handler)
            ],
            # Додайте інші стани за потреби
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(filters.COMMAND, unknown_command)  # Обробка невідомих команд
        ]
    )
    application.add_handler(conv_handler)

    # Додаємо обробник невідомих команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Додаємо обробник тригерних слів
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_trigger_words))

    # Зберігаємо завантажені дані в bot_data
    application.bot_data['heroes_by_class'] = heroes_by_class
    application.bot_data['heroes_data'] = heroes_data

    logger.info("🔄 Бот запущено.")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
        
