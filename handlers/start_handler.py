from telegram import Update
from telegram.ext import CallbackContext
from handlers.start_handler import start

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Я ваш бот для Mobile Legends. Як можу допомогти?')
