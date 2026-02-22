# ДЗ 10: Контейнеризация, автоматизация доставки приложений и сборка образов

Задание по темам 9–10 (DataOps): контейнеризация ML-сервиса Credit Scoring API, лучшие практики Docker, многоэтапная сборка, docker-compose.

---

## Часть 1: Базовый уровень (обязательная)

### Что сделано

1. **Заготовка ML-сервиса** — используется проект Credit Scoring API (`app/main.py`, `app/model.py`).

2. **Dockerfile** (в корне репозитория):
   - Базовый образ: `python:3.12-slim`.
   - Сначала копируется `requirements.txt` и выполняется `pip install` (кэширование слоя при неизменных зависимостях).
   - Затем копируется код `app/`.
   - Порядок COPY соответствует лучшим практикам.

3. **.dockerignore** — исключены `.venv/`, `__pycache__/`, тесты, `hw/`, `terraform/`, `ansible/`, git и прочее, чтобы не раздувать контекст сборки и образ.

4. **Сборка образа и тестовый запрос:**
   ```bash
   docker build -t ml-app:1.0 .
   docker run -d -p 8000:8000 --name ml-app-run ml-app:1.0
   curl http://localhost:8000/health
   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"age":35,"income":60000,"months_on_book":24,"credit_limit":50000}'
   docker stop ml-app-run && docker rm ml-app-run
   ```

5. **docker-compose.yml** — один сервис `ml-app`, сборка из `Dockerfile`, образ `ml-app:1.0`, порт 8000, healthcheck.

6. **Запуск и остановка через docker-compose:**
   ```bash
   docker-compose up -d
   docker-compose down
   ```

---

## Часть 2: Продвинутый уровень (многоэтапная сборка)

### Что сделано

1. **Dockerfile.slim** — многоэтапная сборка:
   - **Этап builder:** в образе `python:3.12-slim` устанавливаются зависимости в каталог wheels (`pip wheel -r requirements.txt`).
   - **Этап runtime:** новый образ копирует только `wheels` и `requirements.txt`, устанавливает пакеты из локального кэша (`pip install --no-index --find-links=/wheels -r requirements.txt`), без обращения в интернет. Затем копируется только код `app/`.

2. **Сборка slim-образа:**
   ```bash
   docker build -f Dockerfile.slim -t ml-app:1.0-slim .
   ```

3. **Сравнение размеров образов** (заполняется после выполнения `docker images`):
   | Образ           | Размер (примерно) | Примечание                          |
   |------------------|-------------------|-------------------------------------|
   | ml-app:1.0       | см. вывод ниже    | Одноэтапная сборка, все слои в одном образе |
   | ml-app:1.0-slim  | см. вывод ниже    | Многоэтапная, в финале только runtime и приложение |

   После сборки выполните и зафиксируйте вывод:
   ```bash
   docker images ml-app
   ```
   Пример вывода:
   ```
   REPOSITORY   TAG        IMAGE ID       CREATED         SIZE
   ml-app       1.0        ...             ...             XXX MB
   ml-app       1.0-slim   ...             ...             YYY MB
   ```
   Ожидаемый эффект: образ `1.0-slim` меньше за счёт отсутствия в финальном образе инструментов сборки и кэша pip; разница обычно порядка десятков мегабайт в зависимости от набора зависимостей.

---

## Часть 3: Задание со звёздочкой

Текущий ML-сервис не требует БД или Redis. Запуск одной командой:

```bash
docker-compose up -d
```

Проверка:
- Документация API: http://localhost:8000/docs  
- Health: http://localhost:8000/health  
- Предсказание: `curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"age":35,"income":60000,"months_on_book":24,"credit_limit":50000}'`

Остановка:
```bash
docker-compose down
```

При необходимости добавить Postgres/Redis — описать сервисы в `docker-compose.yml` и обновить этот раздел в README.

---

## Структура файлов ДЗ 10

```
credit-scoring-model/
├── Dockerfile          # Часть 1: одноэтапная сборка (ml-app:1.0)
├── Dockerfile.slim     # Часть 2: многоэтапная сборка (ml-app:1.0-slim)
├── .dockerignore
├── docker-compose.yml
├── app/
│   ├── main.py
│   └── model.py
├── requirements.txt
├── README.md           # обновлён: ссылка на ДЗ 10
└── docs/
    └── HW10-README.md  # этот файл
```
