terraform {
  required_version = ">= 1.0"
  
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }

  # Backend para armazenar state no OCI Object Storage (recomendado para produção)
  # backend "http" {
  #   address = "https://objectstorage.${var.region}.oraclecloud.com/n/${var.namespace}/b/${var.bucket}/o/terraform.tfstate"
  # }
}

provider "oci" {
  region              = var.region
  config_file_profile = "DEFAULT"
}
