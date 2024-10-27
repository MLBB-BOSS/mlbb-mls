import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Привіт! Я ваш Telegram-бот.")

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
