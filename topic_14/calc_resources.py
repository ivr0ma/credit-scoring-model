#!/usr/bin/env python3
"""
Расчёт ресурсов кластера K8s для ДЗ по теме 14, вариант 1.
Компоненты: БД, кеш, бекенд, фронтенд. Запас 10%.
"""

# Исходные данные вариант 1
COMPONENTS = {
    "db": {"replicas": 3, "ram_gb": 4, "cpu": 1, "kind": "StatefulSet"},
    "cache": {"replicas": 3, "ram_gb": 4, "cpu": 1, "kind": "StatefulSet"},
    "backend": {"replicas": 10, "ram_mb": 600, "cpu": 1, "kind": "Deployment"},
    "frontend": {"replicas": 5, "ram_mb": 50, "cpu": 0.2, "kind": "Deployment"},
}
RESERVE = 0.10  # 10%
MASTER_PER_NODE = {"ram_gb": 4, "cpu": 2}
MASTER_COUNT = 3


def main():
    total_ram_gb = 0.0
    total_cpu = 0.0

    for name, c in COMPONENTS.items():
        if "ram_gb" in c:
            ram = c["replicas"] * c["ram_gb"]
        else:
            ram = c["replicas"] * c["ram_mb"] / 1024
        cpu = c["replicas"] * c["cpu"]
        total_ram_gb += ram
        total_cpu += cpu
        print(f"{name}: RAM {ram:.2f} GB, CPU {cpu}")

    print(f"\nИтого приложение: RAM {total_ram_gb:.2f} GB, CPU {total_cpu}")
    with_reserve_ram = total_ram_gb * (1 + RESERVE)
    with_reserve_cpu = total_cpu * (1 + RESERVE)
    print(f"С запасом {int(RESERVE*100)}%: RAM {with_reserve_ram:.2f} GB, CPU {with_reserve_cpu:.2f}")
    print(f"Округлено: RAM {round(with_reserve_ram)} GB, CPU {round(with_reserve_cpu)}")

    master_ram = MASTER_COUNT * MASTER_PER_NODE["ram_gb"]
    master_cpu = MASTER_COUNT * MASTER_PER_NODE["cpu"]
    print(f"\nMaster ({MASTER_COUNT} нод): {master_ram} GB, {master_cpu} CPU")


if __name__ == "__main__":
    main()
