# Выходные значения для использования в Ansible (inventory)

output "app_instances_public_ips" {
  description = "Публичные IP адреса ВМ приложения"
  value       = yandex_compute_instance.app_vm[*].network_interface[0].nat_ip_address
}

output "app_instances_private_ips" {
  description = "Приватные IP адреса ВМ"
  value       = yandex_compute_instance.app_vm[*].network_interface[0].ip_address
}

output "app_instances_names" {
  description = "Имена ВМ"
  value       = yandex_compute_instance.app_vm[*].name
}

# Для динамического inventory Ansible
output "ansible_hosts" {
  description = "Список хостов для Ansible (user@ip)"
  value       = [for i, ip in yandex_compute_instance.app_vm[*].network_interface[0].nat_ip_address : "ubuntu@${ip}"]
}
