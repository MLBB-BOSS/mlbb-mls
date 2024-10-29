# handlers/guides.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from handlers import States

async def handle_guides_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id
    context.bot_data['last_message_time'][user_id] = context.application.loop.time()
    logger = context.application.job_queue.logger
    logger.info(f"Вибір в Гайдах: {user_input}")
    
    if user_input == "📝 Стратегії для кожного класу":
        await send_class_strategies(update, context)
        return States.GUIDES_MENU
    elif user_input == "💡 Інтерактивні рекомендації":
        await send_interactive_recommendations(update, context)
        return States.GUIDES_MENU
    elif user_input == "🎥 Відео-гайди":
        await send_video_guides(update, context)
        return States.GUIDES_MENU
    elif user_input == "🔙 Назад":
        await start(update, context)
        return States.MAIN_MENU
    else:
        await update.message.reply_text("⚠️ Не вдалося обробити ваш запит.")
        return States.GUIDES_MENU

async def send_class_strategies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    strategies = "📝 **Стратегії для кожного класу:**\n\n" \
                "<b>Танки:</b> Фокусуйтеся на захисті та ініціюванні боїв.\n" \
                "<b>Бійці:</b> Атакуйте ворогів та утримуйте позиції.\n" \
                "<b>Маги:</b> Використовуйте високий урон та контроль.\n" \
                "<b>Стрілеці:</b> Забезпечуйте постійну підтримку з дистанції.\n" \
                "<b>Асасини:</b> Завдавайте швидкий урон та зникайте.\n" \
                "<b>Підтримка:</b> Допомагайте союзникам та контролюйте поле бою.\n\n" \
                "🔗 Детальніше: https://example.com/class-strategies"
    await update.message.reply_text(strategies, parse_mode='HTML', disable_web_page_preview=True)

async def send_interactive_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    classes = ["Танк", "Борець", "Маг", "Стрілець", "Асасин", "Підтримка"]
    buttons = []
    for i in range(0, len(classes), 3):
        row = classes[i:i + 3]
        buttons.append([KeyboardButton(cls) for cls in row])
    buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("💡 **Оберіть клас, щоб отримати рекомендації гайдів:**", parse_mode='Markdown', reply_markup=reply_markup)
    return States.GUIDES_MENU

async def send_video_guides(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_guides = "🎥 **Відео-гайди:**\n\n" \
                  "• [Гайд для новачків](https://youtube.com/guide1)\n" \
                  "• [Стратегії гри](https://youtube.com/guide2)\n" \
                  "• [Поради від професіоналів](https://youtube.com/guide3)\n\n" \
                  "🔗 Детальніше: https://example.com/video-guides"
    await update.message.reply_text(video_guides, parse_mode='Markdown', disable_web_page_preview=True)
