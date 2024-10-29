# utils/recommendations_engine.py
def get_recommendations(hero_class: str) -> str:
    # Приклад простої логіки
    recommendations = {
        "Танк": "Рекомендовані гайди для Танків...",
        "Борець": "Рекомендовані гайди для Бойців...",
        # Додайте інші класи
    }
    return recommendations.get(hero_class, "Немає рекомендацій для цього класу.")
