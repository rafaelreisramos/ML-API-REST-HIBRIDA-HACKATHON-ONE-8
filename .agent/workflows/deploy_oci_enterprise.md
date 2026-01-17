---
description: Deploy da Arquitetura Enterprise (Intel Flex) na OCI para ChurnInsight
---

# 🚀 Workflow: OCI Enterprise Deploy (Intel Flex)

Este workflow descreve o processo de deploy e a arquitetura de alta performance escolhida para o projeto ChurnInsight, utilizando shapes flexíveis Intel na Oracle Cloud Infrastructure.

## 🏛️ Arquitetura Escolhida: Enterprise Flex

Optamos por utilizar a arquitetura **Compute Flexible (Intel Standard 3)** em vez da arquitetura "Micro" (Always Free) ou "Ampere" (ARM), visando a apresentação final e performance garantida.

### Componentes

- **Shape**: `VM.Standard3.Flex` (Intel Ice Lake X9 Platinum).
- **App Server**: 1 OCPU (2 vCPUs) + 8 GB RAM. (Frontend + Backend Java).
- **AI Server**: 2 OCPUs (4 vCPUs) + 16 GB RAM. (Modelo ML Python + Processamento Panda).
- **Storage**: Block Storage de alta performance (50GB+).

### ✅ Vantagens Estratégicas

1. **Performance Pura**: Processadores Intel Ice Lake são significativamente mais rápidos que os AMD E2 (Micro), garantindo que a demo não trave.
2. **Disponibilidade**: Ao contrário dos shapes ARM (Ampere) gratuitos que sofrem com escassez (Out of Capacity), os shapes Intel Enterprise E3/E4 têm alta disponibilidade em São Paulo.
3. **Memória Abundante**: 16GB de RAM no AI Server permite carregar grandes datasets em memória sem OOM (Out of Memory).
4. **Isolamento**: Separação física entre Aplicação Web e Motor de IA garante que picos de processamento no ML não derrubem o Dashboard.

---

## ⚙️ Passo a Passo do Deploy

Para replicar esta infraestrutura do zero:

### 1. Preparação

Certifique-se de ter o OCI CLI configurado e autenticado.

```powershell
oci session authenticate
```

### 2. Configuração Terraform (Enterprise)

Edite `oci-pipeline/terraform/variables.tf` para garantir os recursos pagos (Trial):

```hcl
variable "instance_shape" { default = "VM.Standard3.Flex" } # Intel
variable "ai_ocpus" { default = 2 }      # 4 vCPUs
variable "ai_memory" { default = 16 }    # 16 GB RAM
```

### 3. Provisionamento (IaC)

Execute o pipeline Terraform para criar Rede, Firewall, Storage e Compute.

```powershell
cd oci-pipeline/terraform
# Inicializar
terraform init
# Planejar e Aplicar
terraform apply -auto-approve
```

// turbo

### 4. Verificação de Status

Utilize o script utilitário para checar a saúde das instâncias.

```powershell
.\check_deploy.ps1
```

### 5. Acesso e Manutenção

Consulte o arquivo `OCI_ACCESS_INFO.md` gerado na raiz para obter IPs e chaves.

- **Frontend**: http://<APP_SERVER_IP>
- **SSH**: `ssh opc@<IP_PUBLICO>`

---

## 🔄 Rollback (Plano B)

Se os créditos acabarem ou for necessário voltar ao modo 100% Gratuito:

1. Altere `instance_shape` para `VM.Standard.E2.1.Micro`.
2. Remova os blocos `shape_config` do `main.tf`.
3. Rode `terraform apply`.
