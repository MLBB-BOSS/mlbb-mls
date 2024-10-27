import os
import json

# Список персонажів за ролями
characters = {
    "Tank": [
        "Tigreal", "Khufra", "Gloo", "Atlas", "Edith", "Franco",
        "Gatotkaca", "Hylos", "Barats", "Akai", "Uranus",
        "Johnson", "Minotaur", "Lolita", "Belerick", "Baxia",
        "Grock"
    ],
    "Fighter": [
        "Yin", "Paquito", "Phoveus", "X.Borg", "Cici", "Arlott",
        "Aulus", "Guinivere", "Chou", "Jawhead", "Sun",
        "Roger", "Suyou", "Khaleed", "Aldous", "Balmond",
        "Zilong", "Argus", "Yu Zhong", "Freya", "Lapu-Lapu",
        "Ruby", "Alucard", "Bane", "Alpha", "Leomord",
        "Thamuz", "Badang", "Silvanna", "Terizla",
        "Minsitthar", "Masha"
    ],
    "Marksman": [
        "Hilda", "Dyrroth", "Martis", "Melissa", "Edith",
        "Natan", "Beatrix", "Granger", "Ixia", "Brody",
        "WanWan", "Hanabi", "Bruno", "Miya", "Claude",
        "Yi Sun-Shin", "Layla", "Clint", "Popol & Kupa",
        "Irithel", "Moskov", "Karrie", "Lesley"
    ],
    "Mage": [
        "Kimmy", "Zhuxin", "Esmeralda", "Alice", "Novaria",
        "Xavier", "Valentina", "Harley", "Kagura", "Vale",
        "Zhask", "Eudora", "Luo-Yi", "Yve", "Pharsa",
        "Cyclops", "Chang'e", "Lylia", "Harith", "Kadita",
        "Lunox", "Valir", "Aurora", "Nana", "Vexana",
        "Cecilion", "Gord", "Odette", "Helcurt"
    ],
    "Assassin": [
        "Saber", "Benedetta", "Julian", "Joy", "Arlott",
        "Aamon", "Hayabusa", "Lancelot", "Karina", "Wukong",
        "Yin", "Benedetta", "Fanny", "Saber", "Ling",
        "Gusion", "Nolan", "Lancelot", "Kadita", "Natalia"
    ],
    "Support": [
        "Chip", "Diggie", "Kaja", "Floryn", "Estes",
        "Rafaela", "Mathilda", "Angela", "Carmilla", "Nana"
    ]
}

base_dir = "data/heroes"

for role, heroes in characters.items():
    for hero in heroes:
        # Замінюємо пробіли та спеціальні символи на нижній регістр та підкреслення
        hero_folder = hero.replace(" ", "_").replace("&", "and").lower()
        path = os.path.join(base_dir, role, hero, f"{hero_folder}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({
                    "id": hero_folder,
                    "name": hero,
                    "role": role,
                    "class": "Unknown",
                    "description": "",
                    "stats": {},
                    "skills": {},
                    "emblems": {},
                    "recommended_items": [],
                    "recommended_spells": [],
                    "counter_builds": []
                }, f, ensure_ascii=False, indent=4)
            print(f"Created {path}")
        else:
            print(f"{path} already exists")
                      
