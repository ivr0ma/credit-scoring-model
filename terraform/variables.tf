# ДЗ 6: Инфраструктура как код. Terraform и Ansible
# Переменные для настройки инфраструктуры

variable "yandex_token" {
  description = "OAuth-токен или IAM-токен Yandex Cloud"
  type        = string
  sensitive   = true
}

variable "yandex_cloud_id" {
  description = "Идентификатор облака Yandex Cloud"
  type        = string
}

variable "yandex_folder_id" {
  description = "Идентификатор каталога Yandex Cloud"
  type        = string
}

variable "yandex_zone" {
  description = "Зона доступности"
  type        = string
  default     = "ru-central1-a"
}

variable "instance_count" {
  description = "Количество виртуальных машин для развёртывания приложения (используется count)"
  type        = number
  default     = 2
}

variable "vm_cores" {
  description = "Количество ядер CPU для каждой ВМ"
  type        = number
  default     = 2
}

variable "vm_memory_gb" {
  description = "Объём памяти в ГБ для каждой ВМ"
  type        = number
  default     = 2
}

variable "vm_image_family" {
  description = "Семейство образа ОС (ubuntu-22-04-lts)"
  type        = string
  default     = "ubuntu-22-04-lts"
}

variable "app_port" {
  description = "Порт приложения Credit Scoring API"
  type        = number
  default     = 8000
}

variable "ssh_public_key_path" {
  description = "Путь к файлу с публичным SSH-ключом"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}
