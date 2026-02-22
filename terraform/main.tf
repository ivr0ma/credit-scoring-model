# ДЗ 6: Terraform — описание инфраструктуры
# Используются управляющие конструкции: count, переменные

terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.100"
    }
  }
  required_version = ">= 1.0"
}

provider "yandex" {
  token     = var.yandex_token
  cloud_id  = var.yandex_cloud_id
  folder_id = var.yandex_folder_id
  zone      = var.yandex_zone
}

# Сеть
resource "yandex_vpc_network" "app_network" {
  name = "credit-scoring-network"
}

resource "yandex_vpc_subnet" "app_subnet" {
  name           = "credit-scoring-subnet"
  network_id     = yandex_vpc_network.app_network.id
  zone           = var.yandex_zone
  v4_cidr_blocks = ["10.0.1.0/24"]
}

# Группа безопасности: SSH и доступ к приложению
resource "yandex_vpc_security_group" "app_sg" {
  name       = "credit-scoring-sg"
  network_id = yandex_vpc_network.app_network.id

  ingress {
    description = "SSH"
    port        = 22
    protocol    = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Credit Scoring API"
    port        = var.app_port
    protocol    = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Any"
    protocol    = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

# ВМ создаются через count — несколько одинаковых инстансов
resource "yandex_compute_instance" "app_vm" {
  count       = var.instance_count
  name        = "credit-scoring-app-${count.index + 1}"
  platform_id = "standard-v3"
  zone        = var.yandex_zone

  resources {
    cores  = var.vm_cores
    memory = var.vm_memory_gb * 1024
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.image_id
      size     = 10
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.app_subnet.id
    security_group_ids = [yandex_vpc_security_group.app_sg.id]
    nat                = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file(pathexpand(var.ssh_public_key_path))}"
  }
}

data "yandex_compute_image" "ubuntu" {
  family = var.vm_image_family
}
