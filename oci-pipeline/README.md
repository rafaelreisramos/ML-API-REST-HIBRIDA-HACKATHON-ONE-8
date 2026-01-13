# OCI Deployment Pipeline

Este diretório contém a infraestrutura como código (IaC) para deploy da aplicação ChurnInsight na Oracle Cloud Infrastructure (OCI).

## 📁 Estrutura

```
oci-pipeline/
├── terraform/              # Infraestrutura OCI (Terraform)
│   ├── main.tf            # Configuração principal
│   ├── variables.tf       # Variáveis de entrada
│   ├── outputs.tf         # Outputs do Terraform
│   └── provider.tf        # Configuração do provider OCI
├── .github/workflows/     # GitHub Actions CI/CD
│   └── deploy.yml         # Pipeline de deploy
└── README.md              # Este arquivo
```

## 🚀 Quick Start

### Pré-requisitos

1. **OCI CLI** instalado e configurado
2. **Terraform** >= 1.0
3. **Docker** para build local
4. Credenciais OCI configuradas (`~/.oci/config`)

### Deploy Manual

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Deploy via CI/CD

O pipeline GitHub Actions é acionado automaticamente em:

- Push para `main` (deploy produção)
- Pull Request (validação)

## 🔐 Secrets Necessários

Configure no GitHub (Settings > Secrets):

- `OCI_TENANCY_OCID`
- `OCI_USER_OCID`
- `OCI_FINGERPRINT`
- `OCI_PRIVATE_KEY`
- `OCI_REGION`

## 📦 Recursos Provisionados

- **Container Registry**: Para armazenar imagens Docker
- **Container Instances**: Para rodar os serviços
- **Virtual Cloud Network (VCN)**: Rede isolada
- **Load Balancer**: Distribuição de tráfego
- **Object Storage**: Para logs e backups

## 🔄 Workflow

1. Desenvolvedor faz push para `main`
2. GitHub Actions:
   - Build das imagens Docker
   - Push para OCI Registry
   - Deploy via Terraform
3. Aplicação disponível em produção

## 📊 Monitoramento

- **OCI Monitoring**: Métricas de infraestrutura
- **Logs**: Centralizados no OCI Logging
- **Health Checks**: Configurados no Load Balancer
