import logging
from telegram.ext import Updater, CommandHandler
from config import settings  # Налаштування з конфігураційного файлу
from handlers.start_handler import start  # Імпорт функції start

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Основний запуск бота
def main():
    updater = Updater(settings.TOKEN)
    dispatcher = updater.dispatcher

    # Додаємо обробник для команди /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Запускаємо бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()# Main file for the bot
