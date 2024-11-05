# handlers/help.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.states import States
import logging

logger = logging.getLogger(__name__)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    help_text = """
*Допомога по MLBB Боту*

🦸 *Герої* - інформація про героїв MLBB.
📊 *Статистика* - поточна мета гри, рейтинги героїв.
📖 *Гайди* - стратегії та навчальні матеріали.
🛠 *Збірки* - рекомендовані збірки предметів та емблем.
📰 *Новини* - останні новини та оновлення.
🎉 *Події* - інформація про поточні та майбутні події.
📝 *Вікторини* - тест на знання MLBB.
🏆 *Досягнення* - ваші досягнення у боті.
🌐 *Спільнота* - посилання на MLBB спільноту.
📊 *Опитування* - прийміть участь в опитуваннях.
👤 *Мій Профіль* - перегляньте ваш профіль гравця.
ℹ️ *Допомога* - відобразити це повідомлення.

Введіть команду або оберіть опцію з меню.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
    return States.MAIN_MENU
