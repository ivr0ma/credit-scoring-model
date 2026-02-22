# ДЗ 11–12: GitLab CI/CD

## Что сделано

Настроен пайплайн GitLab CI/CD для проекта credit-scoring-model.

### Файл конфигурации

- **`.gitlab-ci.yml`** — описание пайплайна в корне репозитория.

### Этапы (stages)

1. **lint** — проверка кода линтером (ruff). Запускается при создании/обновлении Merge Request.
2. **test** — запуск тестов (pytest) и сбор покрытия. Артефакты: `junit.xml`, `coverage.xml`.
3. **build** — проверка сборки: импорт модуля и вызов предикта.

### Правила запуска (rules)

- **lint**, **test**: при событиях MR и при пуше в ветку.
- **build**: при пуше в ветку.

### Окружение

- Образ по умолчанию: `python:3.11-slim`.
- В `before_script` устанавливаются зависимости из `requirements.txt`.
- В джобе `test` дополнительно ставятся `pytest`, `pytest-cov`.

### Структура проекта для CI

- `model/` — пакет с логикой скоринга.
- `tests/` — тесты для пайплайна.
- `requirements.txt` — зависимости Python.

## Как проверить локально

```bash
pip install -r requirements.txt
pip install pytest pytest-cov ruff
ruff check .
pytest tests/ -v --cov=model
```

## Валидация конфигурации

В GitLab: **CI/CD → Editor** или **CI/CD → Pipelines** → кнопка **Validate** (CI Lint) для проверки `.gitlab-ci.yml`.
