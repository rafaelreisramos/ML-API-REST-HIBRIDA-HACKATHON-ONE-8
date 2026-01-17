# Credenciais OCI
variable "tenancy_ocid" {
  description = "OCID do Tenancy OCI"
  type        = string
}

variable "user_ocid" {
  description = "OCID do usuário OCI"
  type        = string
  default     = null
}

variable "fingerprint" {
  description = "Fingerprint da chave API OCI"
  type        = string
  default     = null
}

variable "private_key_path" {
  description = "Caminho para a chave privada OCI"
  type        = string
  default     = null
}

variable "region" {
  description = "Região OCI para deploy"
  type        = string
  default     = "sa-saopaulo-1"
}

# Configuração da Aplicação
variable "compartment_ocid" {
  description = "OCID do compartment onde os recursos serão criados"
  type        = string
}

variable "project_name" {
  description = "Nome do projeto (usado como prefixo)"
  type        = string
  default     = "churninsight"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "prod"
}

# Availability Domain (Always Free usa AD específico)
variable "availability_domain" {
  description = "Availability Domain para recursos Always Free"
  type        = string
  default     = "1" # Geralmente AD-1, mas verifique no console
}

# SSH Key para acesso às instâncias
variable "ssh_public_key" {
  description = "Chave SSH pública para acesso às instâncias"
  type        = string
}

# Networking (Always Free)
variable "vcn_cidr" {
  description = "CIDR block para a VCN"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block para a subnet pública"
  type        = string
  default     = "10.0.1.0/24"
}

# Compute (Always Free: 2x VM.Standard.E2.1.Micro)
# Compute (Always Free: 2x VM.Standard.E2.1.Micro)
# Compute (Paid/Trial: VM.Standard.E4.Flex)
variable "instance_shape" {
  description = "Shape Flexivel (AMD E4)"
  type        = string
  default     = "VM.Standard3.Flex"
}

# Recursos App Server (Front + Back)
variable "app_ocpus" {
  type    = number
  default = 1 # 2 vCPUs
}
variable "app_memory" {
  type    = number
  default = 8 # 8 GB RAM
}

# Recursos AI Server (ML Model)
variable "ai_ocpus" {
  type    = number
  default = 2 # 4 vCPUs - Mais poder para ML
}
variable "ai_memory" {
  type    = number
  default = 16 # 16 GB RAM - Mais memória para pandas/sklearn
}

variable "instance_image_ocid" {
  description = "OCID da imagem Oracle Linux 8"
  type        = string
  default     = null
}

# Tags
variable "tags" {
  description = "Tags para recursos OCI"
  type        = map(string)
  default = {
    Project     = "ChurnInsight"
    ManagedBy   = "Terraform"
    Environment = "Production"
    Tier        = "AlwaysFree"
  }
}
