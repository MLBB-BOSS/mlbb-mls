from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Я ваш бот для Mobile Legends. Як можу допомогти?')
