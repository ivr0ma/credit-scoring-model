# ДЗ 8: Конфигурация среды — Ansible + FastAPI в Docker

Проект автоматизирует подготовку сервера (Ubuntu) и развёртывание FastAPI-приложения в Docker.

## Требования

- Ansible
- Коллекция `community.docker`

## Установка зависимостей

```bash
ansible-galaxy collection install -r requirements.yml
```

## Подготовка

1. В файле `inventory` укажите IP целевого сервера (Ubuntu):

   ```ini
   [app_servers]
   fastapi_server ansible_host=84.201.xxx.xxx
   ```

2. Убедитесь, что с управляющей машины доступен SSH по ключу к `ansible_user` (по умолчанию `ubuntu`).

## Запуск

```bash
ansible-playbook -i inventory playbook.yml
```

## Проверка

После успешного выполнения:

```bash
curl http://<server_ip>
```

Ожидаемый ответ: `{"message": "Hello, DevOps World!"}`.

Повторный запуск плейбука должен быть идемпотентным (`changed=0`).
