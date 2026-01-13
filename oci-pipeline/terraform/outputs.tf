# Public IPs
output "app_server_public_ip" {
  description = "IP público do App Server (Frontend + Backend)"
  value       = oci_core_instance.app_server.public_ip
}

output "ai_server_public_ip" {
  description = "IP público do AI Server"
  value       = oci_core_instance.ai_server.public_ip
}

# Application URLs
output "application_url" {
  description = "URL da aplicação (Frontend)"
  value       = "http://${oci_core_instance.app_server.public_ip}"
}

output "backend_api_url" {
  description = "URL da API Backend"
  value       = "http://${oci_core_instance.app_server.public_ip}:9999/graphql"
}

output "ai_service_url" {
  description = "URL do AI Service (interno)"
  value       = "http://${oci_core_instance.ai_server.private_ip}:5000"
}

# Instance IDs
output "app_server_id" {
  description = "OCID do App Server"
  value       = oci_core_instance.app_server.id
}

output "ai_server_id" {
  description = "OCID do AI Server"
  value       = oci_core_instance.ai_server.id
}

# VCN
output "vcn_id" {
  description = "OCID da VCN"
  value       = oci_core_vcn.main.id
}

# Subnet
output "public_subnet_id" {
  description = "OCID da subnet pública"
  value       = oci_core_subnet.public.id
}

# SSH Commands
output "ssh_app_server" {
  description = "Comando SSH para App Server"
  value       = "ssh opc@${oci_core_instance.app_server.public_ip}"
}

output "ssh_ai_server" {
  description = "Comando SSH para AI Server"
  value       = "ssh opc@${oci_core_instance.ai_server.public_ip}"
}
