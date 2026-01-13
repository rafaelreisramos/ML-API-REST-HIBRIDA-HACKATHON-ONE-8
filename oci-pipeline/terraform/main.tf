# ============================================================================
# OCI ALWAYS FREE TIER - INFRAESTRUTURA
# ============================================================================
# Recursos utilizados (dentro do Free Tier):
# - 2x VM.Standard.E2.1.Micro (1 OCPU, 1GB RAM cada)
# - 1x VCN (Virtual Cloud Network)
# - 2x Public IPs
# - 10GB Block Volume (gratuito)
# - Object Storage (20GB gratuito)
# ============================================================================

# ============================================================================
# DATA SOURCES
# ============================================================================

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

# Obter imagem Oracle Linux 8 mais recente
data "oci_core_images" "oracle_linux" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Oracle Linux"
  operating_system_version = "8"
  shape                    = var.instance_shape
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

# ============================================================================
# NETWORKING (Always Free)
# ============================================================================

# Virtual Cloud Network
resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_ocid
  display_name   = "${var.project_name}-vcn-${var.environment}"
  cidr_blocks    = [var.vcn_cidr]
  dns_label      = "${var.project_name}vcn"
  
  freeform_tags = var.tags
}

# Internet Gateway
resource "oci_core_internet_gateway" "main" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-igw"
  enabled        = true
  
  freeform_tags = var.tags
}

# Route Table
resource "oci_core_route_table" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-rt-public"
  
  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.main.id
  }
  
  freeform_tags = var.tags
}

# Security List
resource "oci_core_security_list" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-sl-public"
  
  # SSH
  ingress_security_rules {
    protocol    = "6"
    source      = "0.0.0.0/0"
    stateless   = false
    description = "SSH"
    tcp_options {
      min = 22
      max = 22
    }
  }
  
  # HTTP
  ingress_security_rules {
    protocol    = "6"
    source      = "0.0.0.0/0"
    stateless   = false
    description = "HTTP"
    tcp_options {
      min = 80
      max = 80
    }
  }
  
  # HTTPS
  ingress_security_rules {
    protocol    = "6"
    source      = "0.0.0.0/0"
    stateless   = false
    description = "HTTPS"
    tcp_options {
      min = 443
      max = 443
    }
  }
  
  # Backend API
  ingress_security_rules {
    protocol    = "6"
    source      = "0.0.0.0/0"
    stateless   = false
    description = "Backend API"
    tcp_options {
      min = 9999
      max = 9999
    }
  }
  
  # AI Service
  ingress_security_rules {
    protocol    = "6"
    source      = var.vcn_cidr
    stateless   = false
    description = "AI Service (interno)"
    tcp_options {
      min = 5000
      max = 5000
    }
  }
  
  # Egress - All
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
    stateless   = false
  }
  
  freeform_tags = var.tags
}

# Public Subnet
resource "oci_core_subnet" "public" {
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.main.id
  cidr_block        = var.public_subnet_cidr
  display_name      = "${var.project_name}-subnet-public"
  dns_label         = "public"
  route_table_id    = oci_core_route_table.public.id
  security_list_ids = [oci_core_security_list.public.id]
  
  freeform_tags = var.tags
}

# ============================================================================
# COMPUTE INSTANCES (Always Free: 2x VM.Standard.E2.1.Micro)
# ============================================================================

# VM 1: Frontend + Backend (All-in-One)
resource "oci_core_instance" "app_server" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "${var.project_name}-app-server"
  shape               = var.instance_shape
  
  create_vnic_details {
    subnet_id        = oci_core_subnet.public.id
    display_name     = "app-server-vnic"
    assign_public_ip = true
  }
  
  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.oracle_linux.images[0].id
  }
  
  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data = base64encode(templatefile("${path.module}/cloud-init-app.yaml", {
      project_name = var.project_name
    }))
  }
  
  freeform_tags = var.tags
}

# VM 2: AI Service
resource "oci_core_instance" "ai_server" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "${var.project_name}-ai-server"
  shape               = var.instance_shape
  
  create_vnic_details {
    subnet_id        = oci_core_subnet.public.id
    display_name     = "ai-server-vnic"
    assign_public_ip = true
  }
  
  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.oracle_linux.images[0].id
  }
  
  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data = base64encode(templatefile("${path.module}/cloud-init-ai.yaml", {
      project_name = var.project_name
    }))
  }
  
  freeform_tags = var.tags
}

# ============================================================================
# BLOCK STORAGE (10GB Always Free)
# ============================================================================

resource "oci_core_volume" "app_data" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "${var.project_name}-app-data"
  size_in_gbs         = 10 # Always Free: até 100GB total
  
  freeform_tags = var.tags
}

resource "oci_core_volume_attachment" "app_data_attachment" {
  attachment_type = "paravirtualized"
  instance_id     = oci_core_instance.app_server.id
  volume_id       = oci_core_volume.app_data.id
}
