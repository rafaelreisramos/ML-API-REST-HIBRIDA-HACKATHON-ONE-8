# Credenciais OCI
variable "tenancy_ocid" {
  description = "OCID do Tenancy OCI"
  type        = string
}

variable "user_ocid" {
  description = "OCID do usuário OCI"
  type        = string
}

variable "fingerprint" {
  description = "Fingerprint da chave API OCI"
  type        = string
}

variable "private_key_path" {
  description = "Caminho para a chave privada OCI"
  type        = string
  default     = "~/.oci/oci_api_key.pem"
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
variable "instance_shape" {
  description = "Shape Always Free"
  type        = string
  default     = "VM.Standard.E2.1.Micro" # Always Free
}

variable "instance_image_ocid" {
  description = "OCID da imagem Oracle Linux 8 (Always Free)"
  type        = string
  # Varia por região - obtenha do console ou CLI
  # Exemplo São Paulo: ocid1.image.oc1.sa-saopaulo-1.aaaaaaaa...
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
