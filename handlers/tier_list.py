# handlers/tier_list.py
from telegram import Update
from telegram.ext import ContextTypes

def format_tier_list(tier_list):
    output = ""
    for tier, roles in tier_list.items():
        output += f"{tier}-рівень:\n\n"
        for role, heroes in roles.items():
            output += f"{role}:\n\n"
            for hero_info in heroes:
                hero_name = hero_info["name"]
                build = ", ".join(hero_info["build"])
                output += f"- {hero_name}\n  Білд: {build}\n\n"
            output += "\n"
        output += "\n"
    return output

async def send_tier_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Оновлений тир-лист з білдами
    tier_list = {
        "S": {
            "Танки": [
                {"name": "Khufra", "build": ["Tough Boots", "Cursed Helmet", "Antique Cuirass", "Dominance Ice", "Immortality", "Athena's Shield"]},
                {"name": "Atlas", "build": ["Tough Boots", "Cursed Helmet", "Guardian Helmet", "Antique Cuirass", "Immortality", "Athena's Shield"]},
                {"name": "Tigreal", "build": ["Warrior Boots", "Antique Cuirass", "Dominance Ice", "Immortality", "Athena's Shield", "Guardian Helmet"]},
                {"name": "Fredrinn", "build": ["Warrior Boots", "Bloodlust Axe", "Antique Cuirass", "Dominance Ice", "Immortality", "Athena's Shield"]},
                {"name": "Gatotkaca", "build": ["Tough Boots", "Cursed Helmet", "Athena's Shield", "Antique Cuirass", "Immortality", "Oracle"]},
            ],
            "Бійці": [
                {"name": "Paquito", "build": ["Warrior Boots", "Bloodlust Axe", "Blade of Despair", "Hunter Strike", "Malefic Roar", "Immortality"]},
                {"name": "Yin", "build": ["Warrior Boots", "Bloodlust Axe", "Blade of Despair", "Hunter Strike", "Malefic Roar", "Immortality"]},
                {"name": "Arlott", "build": ["Warrior Boots", "Bloodlust Axe", "Blade of Despair", "Hunter Strike", "Malefic Roar", "Immortality"]},
                {"name": "Ruby", "build": ["Warrior Boots", "Bloodlust Axe", "Oracle", "Queen's Wings", "Immortality", "Athena's Shield"]},
                {"name": "Sun", "build": ["Warrior Boots", "Corrosion Scythe", "Demon Hunter Sword", "Golden Staff", "Malefic Roar", "Immortality"]},
            ],
            "Убивці": [
                {"name": "Helcurt", "build": ["Raptor Machete", "Warrior Boots", "Blade of Despair", "Endless Battle", "Malefic Roar", "Queen's Wings"]},
                {"name": "Julian", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Saber", "build": ["Warrior Boots", "Blade of Despair", "Endless Battle", "Hunter Strike", "Malefic Roar", "Immortality"]},
                {"name": "Joy", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Benedetta", "build": ["Warrior Boots", "Bloodlust Axe", "Blade of Despair", "Hunter Strike", "Malefic Roar", "Immortality"]},
            ],
            "Стрільці": [
                {"name": "Beatrix", "build": ["Swift Boots", "Blade of Despair", "Endless Battle", "Malefic Roar", "Immortality", "Athena's Shield"]},
                {"name": "Granger", "build": ["Swift Boots", "Blade of Despair", "Endless Battle", "Malefic Roar", "Immortality", "Athena's Shield"]},
                {"name": "Melissa", "build": ["Swift Boots", "Demon Hunter Sword", "Golden Staff", "Corrosion Scythe", "Malefic Roar", "Immortality"]},
                {"name": "Natan", "build": ["Swift Boots", "Demon Hunter Sword", "Golden Staff", "Corrosion Scythe", "Malefic Roar", "Immortality"]},
                {"name": "Roger", "build": ["Swift Boots", "Windtalker", "Demon Hunter Sword", "Blade of Despair", "Malefic Roar", "Immortality"]},
            ],
            "Маги": [
                {"name": "Alice", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Valentina", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Esmeralda", "build": ["Arcane Boots", "Enchanted Talisman", "Calamity Reaper", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Zhuxin", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
                {"name": "Novaria", "build": ["Arcane Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Blood Wings"]},
            ],
            "Підтримка": [
                {"name": "Mathilda", "build": ["Arcane Boots", "Enchanted Talisman", "Fleeting Time", "Holy Crystal", "Divine Glaive", "Immortality"]},
                {"name": "Floryn", "build": ["Arcane Boots", "Enchanted Talisman", "Oracle", "Dominance Ice", "Immortality", "Athena's Shield"]},
                {"name": "Kaja", "build": ["Warrior Boots", "Clock of Destiny", "Lightning Truncheon", "Holy Crystal", "Divine Glaive", "Immortality"]},
                {"name": "Angela", "build": ["Arcane Boots", "Enchanted Talisman", "Fleeting Time", "Oracle", "Immortality", "Athena's Shield"]},
                {"name": "Diggie", "build": ["Arcane Boots", "Enchanted Talisman", "Dominance Ice", "Immortality", "Athena's Shield", "Oracle"]},
            ],
        },
        "A": {
            "Танки": [
                {"name": "Gatotkaca", "build": []},
                {"name": "Belerick", "build": []},
                {"name": "Johnson", "build": []},
                {"name": "Akai", "build": []},
                {"name": "Uranus", "build": []},
            ],
            "Бійці": [
                {"name": "Chou", "build": []},
                {"name": "Leomord", "build": []},
                {"name": "Thamuz", "build": []},
                {"name": "Dyrroth", "build": []},
                {"name": "Aulus", "build": []},
            ],
            "Убивці": [
                {"name": "Hayabusa", "build": []},
                {"name": "Karina", "build": []},
                {"name": "Gusion", "build": []},
                {"name": "Ling", "build": []},
                {"name": "Lancelot", "build": []},
            ],
            "Стрільці": [
                {"name": "Karrie", "build": []},
                {"name": "Claude", "build": []},
                {"name": "Layla", "build": []},
                {"name": "Yi Sun-shin", "build": []},
                {"name": "Brody", "build": []},
            ],
            "Маги": [
                {"name": "Kagura", "build": []},
                {"name": "Lunox", "build": []},
                {"name": "Pharsa", "build": []},
                {"name": "Harith", "build": []},
                {"name": "Chang'e", "build": []},
            ],
            "Підтримка": [
                {"name": "Rafaela", "build": []},
                {"name": "Estes", "build": []},
                {"name": "Carmilla", "build": []},
                {"name": "Faramis", "build": []},
                {"name": "Lolita", "build": []},
            ],
        },
    }

    formatted_list = format_tier_list(tier_list)

    # Надсилаємо повідомлення з тир-листом у форматі кодового блоку
    await update.message.reply_text(f"```\n{formatted_list}\n```", parse_mode="Markdown")
    
