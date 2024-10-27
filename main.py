import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import settings  # Налаштування з конфігураційного файлу

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функції команд
def start(update, context):
    update.message.reply_text('Привіт! Я бот. Як можу допомогти?')

# Основний запуск бота
def main():
    updater = Updater(settings.TOKEN)
    dispatcher = updater.dispatcher

    # Додаємо обробники команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Запускаємо бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()# Main file for the bot
