# Helm-чарт nginx (ДЗ 15, DataOps — Helm)

Чарт реализует требования задания:
1. Helm-чарт для nginx.
2. Версия образа задаётся через `values` (поле `image.repository` и `image.tag`).
3. Лимиты и риквесты CPU/memory задаются через `resources.limits` и `resources.requests` (при отсутствии блок не добавляется).
4. Генерация манифеста Ingress включается/выключается флагом `ingress.enabled`.

## Структура

```
nginx/
├── Chart.yaml
├── values.yaml           # значения по умолчанию
├── values-minimal.yaml   # пример: без ресурсов, без Ingress
├── values-with-resources.yaml
├── values-with-ingress.yaml
├── values-full.yaml
├── README.md
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml      # рендерится только при ingress.enabled: true
    └── NOTES.txt
```

## Параметры (values)

| Параметр | Описание |
|----------|----------|
| `image.repository` | Репозиторий образа (например, `nginx`) |
| `image.tag` | Тег образа (версия, п.2) |
| `resources.limits` / `resources.requests` | CPU/memory (п.3). Не задавать — блок ресурсов не создаётся |
| `ingress.enabled` | `true` — создаётся Ingress, `false` — манифест не генерируется (п.4) |
| `ingress.hosts`, `ingress.className`, `ingress.tls` | Настройки Ingress при `ingress.enabled: true` |

## Деплой в кластер (п.5)

Убедитесь, что настроен `kubectl` и установлен Helm 3.

**1. Минимальный деплой (образ по умолчанию, без ресурсов, без Ingress):**
```bash
helm install nginx-min ./nginx -f nginx/values-minimal.yaml -n dev --create-namespace
```

**2. С лимитами и риквестами и другой версией образа:**
```bash
helm install nginx-res ./nginx -f nginx/values-with-resources.yaml -n dev --create-namespace
```

**3. С включённым Ingress:**
```bash
helm install nginx-ing ./nginx -f nginx/values-with-ingress.yaml -n dev --create-namespace
```

**4. Полная конфигурация (другая версия, ресурсы, Ingress, 2 реплики):**
```bash
helm install nginx-full ./nginx -f nginx/values-full.yaml -n prod --create-namespace
```

**Переопределение через `--set`:**
```bash
helm install nginx-custom ./nginx -n dev --create-namespace \
  --set image.tag=1.24 \
  --set resources.limits.cpu=300m \
  --set resources.limits.memory=192Mi \
  --set ingress.enabled=true
```

**Проверка манифестов без установки:**
```bash
helm template nginx ./nginx
helm template nginx ./nginx -f nginx/values-with-resources.yaml
helm template nginx ./nginx --set ingress.enabled=false
```

**Обновление релиза:**
```bash
helm upgrade nginx-min ./nginx -f nginx/values-with-resources.yaml -n dev
```

**Удаление:**
```bash
helm uninstall nginx-min -n dev
```

## Самопроверка

- [ ] `helm template nginx ./nginx` выводит Deployment, Service; Ingress нет (ingress.enabled по умолчанию false).
- [ ] С `-f values-with-resources.yaml` в Deployment есть `resources.limits` и `resources.requests`.
- [ ] С `-f values-with-ingress.yaml` в выводе есть манифест Ingress.
- [ ] С `--set image.tag=1.24` в образе подставляется указанный тег.
- [ ] Деплой в кластер каждым из вариантов (разные неймспейсы или имена релизов) выполняется без ошибок.
