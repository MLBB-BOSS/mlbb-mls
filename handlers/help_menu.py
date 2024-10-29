# handlers/help_menu.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers import States

async def handle_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger = context.application.job_queue.logger
    logger.info(f"Вибір в Допомозі: {user_input}")
    
    if user_input == "❓ FAQ":
        await send_faq(update, context)
        return States.HELP_MENU
    elif user_input == "💬 Живий чат підтримки":
        await send_live_support(update, context)
        return States.HELP_MENU
    elif user_input == "🐞 Повідомлення про помилки":
        await send_bug_report(update, context)
        return States.HELP_MENU
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.HELP_MENU

async def send_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    faq = "❓ **FAQ:**\n\n" \
          "• **Як зареєструватися?** Перейдіть за посиланням реєстрації.\n" \
          "• **Як обрати героя?** Вивчіть характеристики героїв у розділі Персонажі.\n" \
          "• **Що робити при багах?** Використовуйте форму повідомлення про помилки.\n\n" \
          "🔗 Детальніше: https://example.com/faq"
    await update.message.reply_text(faq, parse_mode='HTML', disable_web_page_preview=True)

async def send_live_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    live_support = "💬 **Живий чат підтримки:**\n\n" \
                   "Якщо у вас виникли проблеми або запитання, зверніться до нашої підтримки:\n\n" \
                   "🔗 [Підтримка](https://t.me/your_support_chat)"
    await update.message.reply_text(live_support, parse_mode='HTML', disable_web_page_preview=True)

async def send_bug_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bug_report = "🐞 **Повідомлення про помилки:**\n\n" \
                 "Якщо ви знайшли баг або маєте пропозиції, будь ласка, заповніть наступну форму:\n\n" \
                 "🔗 [Повідомити про помилку](https://example.com/report-bug)"
    await update.message.reply_text(bug_report, parse_mode='HTML', disable_web_page_preview=True)
