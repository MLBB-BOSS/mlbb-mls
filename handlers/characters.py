# handlers/characters.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def handle_selecting_hero_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_class = update.message.text.strip()
    heroes_by_class = context.bot_data.get('heroes_by_class', {})

    # Перевірка, чи користувач вибрав опцію з головного меню
    main_menu_options = ["🦸 Герої", "📊 Статистика", "📖 Гайди", "🛠 Збірки", "📰 Новини", "🎉 Події",
                         "📝 Вікторини", "🏆 Досягнення", "🌐 Спільнота", "📊 Опитування", "👤 Мій Профіль",
                         "ℹ️ Допомога", "🔍 Пошук"]

    if selected_class in main_menu_options:
        from handlers.main_menu import main_menu_handler
        await main_menu_handler(update, context)
        return States.MAIN_MENU

    if selected_class == "🔙 Назад":
        from handlers.main_menu import get_main_menu_keyboard
        reply_markup = get_main_menu_keyboard()
        await update.message.reply_text("🔙 Повернення до головного меню:", reply_markup=reply_markup)
        return States.MAIN_MENU

    if selected_class not in heroes_by_class:
        await update.message.reply_text("⚠️ Будь ласка, виберіть клас з меню.")
        return States.SELECTING_HERO_CLASS

    context.user_data['selected_class'] = selected_class
    heroes = heroes_by_class[selected_class]

    # Логування списку героїв
    logger.info(f"Heroes in class {selected_class}: {heroes}")

    if not heroes:
        await update.message.reply_text(f"⚠️ Немає доступних героїв у класі {selected_class}.")
        return States.SELECTING_HERO_CLASS

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
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(f"Виберіть героя з класу {selected_class}:", reply_markup=reply_markup)
    return States.SELECTING_HERO
