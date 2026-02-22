# ДЗ по теме 13: Мониторинг и логирование

Реализован стек мониторинга и сбора логов: **Prometheus**, **Grafana**, **Loki**, **Promtail**.

## Структура

- `docker-compose.yml` — сервисы: Prometheus, Loki, Promtail, Grafana, log-generator (пример приложения с отчётами на диск).
- `monitoring/prometheus/prometheus.yml` — конфигурация сбора метрик (Prometheus, Loki, Promtail).
- `monitoring/loki/loki-config.yaml` — конфигурация Loki.
- `monitoring/promtail/promtail-config.yaml` — сбор логов из `logs/`, парсинг формата `[date time] [tenant] [severity] [module] [message]`, отправка в Loki.
- `monitoring/grafana/provisioning/datasources/datasources.yml` — автоматическое подключение источников Prometheus и Loki в Grafana.
- `logs/app.log` — пример логов приложения (и папка для логов от log-generator).

## Запуск

Из корня репозитория:

```bash
docker compose up -d
```

Проверка:

- **Grafana**: http://localhost:3000 (логин/пароль: `admin` / `admin`).
- **Prometheus**: http://localhost:9090.
- **Loki**: http://localhost:3100/ready.

## Что сделано

1. **Prometheus** — сбор метрик с себя, Loki и Promtail (`scrape_configs`).
2. **Loki** — приём и хранение логов.
3. **Promtail** — чтение логов из `logs/`, парсинг по regex, метки `tenantid`, `severity`, `module`, парсинг времени, отправка в Loki.
4. **Grafana** — provisioning источников данных Prometheus (по умолчанию) и Loki.
5. **log-generator** — контейнер, который пишет логи в формате отчётов в `logs/app.log` (имитация платформы с отчётами на диск).
6. Для всех сервисов заданы `container_name` для удобного отображения в Grafana.

## Просмотр логов в Grafana

1. Открыть **Explore** (иконка компаса).
2. Выбрать источник **Loki**.
3. Запрос, например: `{job="logs"}` или с фильтром: `{job="logs", severity="INFO"}`.

Метрики можно смотреть в том же **Explore**, выбрав источник **Prometheus**.
