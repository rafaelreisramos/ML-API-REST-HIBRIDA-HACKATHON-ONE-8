# 🌍 Próximos Passos: Infraestrutura OCI com Terraform

Este documento define o escopo para a provisão da infraestrutura do **ChurnInsight** na **Oracle Cloud Infrastructure (OCI)**.

## 🎯 Objetivo

Migrar a aplicação para a OCI utilizando Terraform, garantindo uma arquitetura robusta, segura e escalável, aproveitando o poder da nuvem Oracle.

## 🏗️ Arquitetura Alvo (OCI - Oracle Cloud)

### 1. Rede e Segurança (Networking)

* **VCN (Virtual Cloud Network)**: Criação de uma rede isolada na região.
* **Subnets**: Separação entre pública (Load Balancer) e privada (Aplicações e Banco).
* **Security Lists / NSGs**: Controle fino de tráfego (Firewall virtual).

### 2. Computação (Compute & Containers)

* **OCIR (OCI Registry)**: Armazenamento seguro das imagens Docker (`backend`, `ai-service`, `frontend`).
* **OCI Container Instances**: Execução de containers serverless para alta performance e simplicidade de gestão (sem necessidade de gerenciar VMs).
  * *Alternativa Enterprise*: **OKE (Oracle Kubernetes Engine)** para orquestração avançada.

### 3. Banco de Dados (Persistence)

* **OCI Database for PostgreSQL**: Serviço gerenciado de PostgreSQL da Oracle.
  * Alta disponibilidade e backups automáticos.
  * Integração nativa com a VCN para segurança máxima (sem acesso público).

### 4. Entrega e Acesso

* **OCI Load Balancer**: Balanceamento de carga Layer 7 (HTTP/HTTPS) distribuindo tráfego para as instâncias de container.
* **WAF (Web Application Firewall)**: Proteção contra ataques web no Load Balancer.

## 📋 Checklist Terraform para OCI

Na próxima sessão, focaremos em:

* [ ] **OCI Provider**: Configuração de autenticação (Tenancy OCID, User OCID, Private Key).
* [ ] **Compartments**: Organização lógica dos recursos (ex: `Hackathon_Project`).
* [ ] **Networking Module**: Criação da VCN, Internet Gateway (IGW), NAT Gateway e Route Tables.
* [ ] **Database Module**: Provisionamento do cluster PostgreSQL gerenciado.
* [ ] **Compute Module**: Definição das Container Instances com injeção de variáveis de ambiente.

## 🚀 Diferenciais OCI

* **Custo-Benefício**: Aproveitar instâncias ARM (Ampere) se compatível, ou Flex Shapes.
* **Performance**: Rede de baixa latência da OCI.
* **Segurança**: Criptografia por padrão (at rest e in transit).

---
*Documento atualizado para OCI.*
