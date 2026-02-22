"""Предикт по фичам (заглушка для пайплайна CI/CD)."""


def predict(features: list) -> float:
    """Возвращает «скор» по списку фичей (заглушка)."""
    if not features:
        return 0.0
    # Простая линейная комбинация для демо
    return min(1.0, max(0.0, sum(features) / max(len(features), 1)))
