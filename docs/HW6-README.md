# ДЗ 6: Инфраструктура как код. Terraform и Ansible

Развёртывание **Credit Scoring API** с помощью Terraform (создание инфраструктуры в Yandex Cloud) и Ansible (конфигурация серверов и деплой приложения).

---

## Что сделано

### Terraform

- **Переменные** (`variables.tf`) — токен, cloud_id, folder_id, зона, количество ВМ, ресурсы CPU/RAM, образ ОС, порт приложения, путь к SSH-ключу.
- **Управляющая конструкция `count`** — создаётся несколько одинаковых ВМ (`credit-scoring-app-1`, `credit-scoring-app-2`, …) без дублирования кода.
- **Ресурсы**: сеть, подсеть, группа безопасности (SSH + порт приложения), ВМ на Ubuntu 22.04.
- **Outputs** — публичные и приватные IP, имена ВМ, список `ubuntu@IP` для Ansible.

### Ansible

- **Playbook** (`ansible/playbook.yml`) — запуск роли на группе хостов `app_servers`.
- **Роль `credit_scoring_app`**:
  - установка Python3, pip, venv;
  - создание каталога приложения и копирование кода;
  - создание venv и установка зависимостей из `requirements.txt`;
  - шаблон **Jinja2** для unit systemd (`.j2`);
  - включение и запуск сервиса, проверка `/health`.
- **Инвентарь** — статический `inventory/hosts.yml` или динамическое формирование из вывода Terraform.

---

## Требования

- [Terraform](https://www.terraform.io/) >= 1.0
- [Ansible](https://www.ansible.com/) >= 2.14
- Аккаунт Yandex Cloud, OAuth- или IAM-токен
- SSH-ключ с публичной частью (например `~/.ssh/id_rsa.pub`)

---

## Порядок выполнения

### 1. Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Отредактируйте terraform.tfvars: токен, cloud_id, folder_id

terraform init
terraform plan
terraform apply
```

Сохраните вывод (например, публичные IP):

```bash
terraform output ansible_hosts
```

### 2. Заполнить инвентарь Ansible

Вариант А — вручную отредактировать `ansible/inventory/hosts.yml`, подставив IP из `terraform output app_instances_public_ips`.

Вариант Б — сгенерировать JSON для динамического inventory из вывода Terraform (скрипт `inventory/terraform_inventory.py` или использование [terraform-inventory](https://github.com/adammck/terraform-inventory)).

### 3. Ansible

Из корня проекта (чтобы роль видела код приложения):

```bash
cd ansible
ansible-playbook playbook.yml
```

Проверка:

```bash
curl http://<PUBLIC_IP>:8000/health
curl -X POST http://<PUBLIC_IP>:8000/predict -H "Content-Type: application/json" -d '{"age":35,"income":60000,"months_on_book":24,"credit_limit":50000}'
```

---

## Структура

```
credit-scoring-model/
├── terraform/
│   ├── main.tf           # provider, сеть, SG, ВМ (count)
│   ├── variables.tf      # переменные
│   ├── outputs.tf        # IP и хосты для Ansible
│   └── terraform.tfvars.example
├── ansible/
│   ├── ansible.cfg
│   ├── playbook.yml
│   ├── inventory/
│   │   ├── hosts.yml
│   │   └── terraform_inventory.py
│   └── roles/
│       └── credit_scoring_app/
│           ├── tasks/main.yml
│           ├── templates/credit-scoring-api.service.j2
│           └── defaults/main.yml
└── docs/
    └── HW6-README.md     # этот файл
```

---

## Безопасность

- В репозитории не храните `terraform.tfvars` с токенами; используйте переменные окружения или CI/CD secrets.
- Файлы `*.tfstate` и `*.tfstate.backup` добавьте в `.gitignore`.
