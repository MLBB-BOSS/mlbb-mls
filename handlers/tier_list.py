# handlers/tier_list.py
from telegram import Update
from telegram.ext import ContextTypes

def format_tier_list(tier_list):
    output = ""
    for tier, roles in tier_list.items():
        output += f"{tier}-рівень:\n\n"
        for role, heroes in roles.items():
            output += f"{role}:\n"
            for hero in heroes:
                output += f"- {hero}\n"
            output += "\n"
    return output

async def send_tier_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Приклад тир-листа
    tier_list = {
        "S": {
            "Танки": ["Мінотаур"],
            "Бійці": ["Сую", "Їнь"],
            "Убивці": ["Хаябуса", "Лінг", "Сейбер", "Фанні"],
            "Стрільці": ["Роджер", "Пополь і Купа"],
            "Маги": ["Лілія", "Кагура"],
            "Підтримка": ["Матильда", "Анджела"],
        },
        "A": {
            "Танки": ["Тигріл", "Гатоткача"],
            "Бійці": ["Чоу", "Рубі"],
            "Убивці": ["Гусіон", "Ланселот"],
            "Стрільці": ["Керрі", "Грейнджер"],
            "Маги": ["Аліса", "Одетта"],
            "Підтримка": ["Рафаель", "Діггі"],
        },
        # Додайте інші рівні та героїв за потреби
    }

    formatted_list = format_tier_list(tier_list)

    # Надсилаємо повідомлення з тир-листом у форматі кодового блоку
    await update.message.reply_text(f"```\n{formatted_list}\n```", parse_mode="Markdown")
  
