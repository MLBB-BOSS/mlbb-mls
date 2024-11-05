# handlers/tier_list.py
from telegram import Update
from telegram.ext import ContextTypes

async def send_tier_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Оновлена інформація про мету
    tier_list_text = """
На основі останніх даних щодо актуальної мети Mobile Legends Bang Bang від 5 листопада 2024 року, сформований структурований перелік героїв з найкращими білдами, емблемами та рекомендаціями заклинань.
_______________________

• S-клас (Найсильніші герої)
_______________________

Асасини:

• Ланселот, Аамон, Лінг, Сабер

• Емблема - Assassin Emblem з талантами на фізичний урон та проникнення.

• Предмети - Blade of Despair, Malefic Roar, Hunter Strike, Endless Battle.

• Заклинання - Retribution або Flicker.

_______________________

Маги:

• Валентина, Фарса, Харлі

• Емблема - Mage Emblem з талантами на магічний урон.

• Предмети - Clock of Destiny, Holy Crystal, Divine Glaive.

• Заклинання - Flicker.

_______________________

Стрільці:

• Едіт, Грейнджер, Клінт

• Емблема - Marksman Emblem з талантами на проникнення.

• Предмети - Blade of Despair, Endless Battle, Malefic Roar.

• Заклинання - Flicker.

_______________________

Танки:

• Атлас, Тигріал, Грок

• Емблема - Tank Emblem для витривалості.

• Предмети - Cursed Helmet, Immortality, Dominance Ice.

• Заклинання - Flicker.

_______________________

Підтримка:

• Флорін, Матільда, Діггі

• Емблема - Support Emblem з фокусом на зменшення часу відновлення.

• Предмети - Enchanted Talisman, Fleeting Time, Athena's Shield.

• Заклинання - Flicker.

_______________________

A-клас (Сильні герої)
_______________________

Асасини:

• Хаябуса, Фанні, Каріна, Хелкерт

• Емблема - Assassin Emblem для підвищення фізичного урону.

• Предмети - Hunter Strike, Blade of Despair, Immortality.

• Заклинання - Retribution або Flicker.

_______________________

Бійці:

• Чоу, Ю Чжун, Дайрот

• Емблема - Fighter Emblem з фокусом на витривалість.

• Предмети - War Axe, Bloodlust Axe, Queen’s Wings.

• Заклинання - Flicker.

_______________________

Маги:

• Вале, Ів, Кагура

• Емблема - Mage Emblem з фокусом на магічний урон.

• Предмети - Lightning Truncheon, Clock of Destiny, Blood Wings.

• Заклинання - Flicker.

_______________________

Стрільці:

• Броуді, Іксія, Беатрікс

• Емблема - Marksman Emblem для швидкості атаки.

• Предмети - Malefic Roar, Blade of Despair, Windtalker.

• Заклинання - Flicker.

_______________________

Танки:

• Франко, Аккай, Уранус

• Емблема - Tank Emblem для витривалості.

• Предмети - Immortality, Athena's Shield, Dominance Ice.

• Заклинання - Flicker.

_______________________

Підтримка:

• Естес, Анджела, Кадж

• Емблема - Support Emblem для захисту союзників.

• Предмети - Necklace of Durance, Fleeting Time, Immortality.

• Заклинання - Flicker.

_______________________

Цей структурований перелік надає актуальну інформацію про найсильніших героїв Mobile Legends, враховуючи останні зміни та оновлення у грі.
"""

    # Екранування спеціальних символів для MarkdownV2
    def escape_markdown(text):
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
        return ''.join(['\\' + char if char in escape_chars else char for char in text])

    escaped_text = escape_markdown(tier_list_text)

    # Надсилаємо повідомлення з тир-листом у кодовому блоці Java
    await update.message.reply_text(f"```java\n{escaped_text}\n```", parse_mode="MarkdownV2")
