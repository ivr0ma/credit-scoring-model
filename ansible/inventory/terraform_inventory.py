#!/usr/bin/env python3
"""
Динамический inventory для Ansible из вывода Terraform (ДЗ 6).
Использование:
  terraform -chdir=../terraform output -raw ansible_hosts | python3 terraform_inventory.py
  или: export TF_OUTPUT=$(terraform -chdir=../terraform output -json) и парсить JSON.

Упрощённый вариант: читает список хостов из stdin (по одному на строку, формат ubuntu@IP).
"""
import json
import sys

def main():
    hosts = []
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Формат: ubuntu@1.2.3.4
        if "@" in line:
            user, ip = line.split("@", 1)
            hosts.append({"host": ip, "user": user})
        else:
            hosts.append({"host": line, "user": "ubuntu"})

    inventory = {
        "app_servers": {
            "hosts": {f"app{i+1}": {"ansible_host": h["host"], "ansible_user": h["user"]} for i, h in enumerate(hosts)},
            "vars": {"app_port": 8000, "app_name": "credit-scoring-api"}
        },
        "_meta": {"hostvars": {}}
    }
    for name, data in inventory["app_servers"]["hosts"].items():
        inventory["_meta"]["hostvars"][name] = data

    print(json.dumps(inventory, indent=2))

if __name__ == "__main__":
    main()
