# 🚀 Guia Rápido de Deploy OCI

## Pré-requisitos

1. **Conta OCI** ativa
2. **OCI CLI** instalado e configurado
3. **Terraform** >= 1.0 instalado
4. **Docker** instalado (para build local)

## 📋 Passo a Passo

### 1. Configurar Credenciais OCI

```bash
# Configurar OCI CLI (interativo)
oci setup config

# Ou criar manualmente ~/.oci/config:
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaaxxxxxxxx
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
tenancy=ocid1.tenancy.oc1..aaaaaaaaxxxxxxxx
region=sa-saopaulo-1
key_file=~/.oci/oci_api_key.pem
```

### 2. Obter Informações Necessárias

No Console OCI, obtenha:

- **Tenancy OCID**: Menu > Tenancy Details
- **User OCID**: Menu > User Settings
- **Compartment OCID**: Menu > Identity > Compartments
- **Registry Namespace**: Menu > Developer Services > Container Registry

### 3. Configurar Variáveis Terraform

```bash
cd oci-pipeline/terraform
cp terraform.tfvars.example terraform.tfvars

# Editar terraform.tfvars com seus valores
nano terraform.tfvars
```

### 4. Deploy da Infraestrutura

```bash
# Inicializar Terraform
terraform init

# Validar configuração
terraform validate

# Visualizar plano
terraform plan

# Aplicar (criar recursos)
terraform apply
```

### 5. Build e Push das Imagens Docker

```bash
# Voltar para raiz do projeto
cd ../..

# Login no OCI Registry
docker login sa-saopaulo-1.ocir.io \
  -u '<namespace>/<username>' \
  -p '<auth-token>'

# Build e Push AI Service
docker build -t sa-saopaulo-1.ocir.io/<namespace>/churninsight/ai-service:latest \
  -f ai_service/Dockerfile .
docker push sa-saopaulo-1.ocir.io/<namespace>/churninsight/ai-service:latest

# Build e Push Backend
./mvnw clean package -DskipTests
docker build -t sa-saopaulo-1.ocir.io/<namespace>/churninsight/backend:latest \
  -f Dockerfile.backend .
docker push sa-saopaulo-1.ocir.io/<namespace>/churninsight/backend:latest

# Build e Push Frontend
docker build -t sa-saopaulo-1.ocir.io/<namespace>/churninsight/frontend:latest \
  frontend/
docker push sa-saopaulo-1.ocir.io/<namespace>/churninsight/frontend:latest
```

### 6. Atualizar Container Instances

Após o push das imagens, force o restart dos containers:

```bash
cd oci-pipeline/terraform
terraform apply -replace=oci_container_instances_container_instance.ai_service
terraform apply -replace=oci_container_instances_container_instance.backend
terraform apply -replace=oci_container_instances_container_instance.frontend
```

### 7. Acessar Aplicação

```bash
# Obter URL pública
terraform output application_url

# Exemplo de output:
# http://xxx.xxx.xxx.xxx
```

## 🔄 CI/CD Automático (GitHub Actions)

### Configurar Secrets no GitHub

1. Acesse: `Settings > Secrets and variables > Actions`
2. Adicione os seguintes secrets:

```
OCI_TENANCY_OCID
OCI_USER_OCID
OCI_FINGERPRINT
OCI_PRIVATE_KEY (conteúdo completo do arquivo .pem)
OCI_REGION
OCI_COMPARTMENT_OCID
OCI_REGISTRY_NAMESPACE
OCI_REGISTRY_USERNAME (namespace/username)
OCI_REGISTRY_PASSWORD (Auth Token)
```

### Trigger do Deploy

```bash
# Push para main dispara deploy automático
git push origin main

# Ou trigger manual via GitHub UI:
# Actions > Deploy to OCI > Run workflow
```

## 🧹 Destruir Recursos (Cleanup)

```bash
cd oci-pipeline/terraform
terraform destroy
```

## 📊 Monitoramento

- **OCI Console**: Monitoring > Metrics
- **Logs**: Logging > Log Groups
- **Container Instances**: Developer Services > Container Instances

## 🆘 Troubleshooting

### Erro: "Service limit exceeded"

Aumente os limites de serviço no console OCI ou use shapes menores.

### Erro: "Authentication failed"

Verifique se o Auth Token está correto e não expirou.

### Container não inicia

Verifique os logs:

```bash
oci logging-search search-logs \
  --search-query "search \"<compartment-ocid>/container-instances\""
```

## 📚 Recursos Adicionais

- [OCI Documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Terraform OCI Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)
- [OCI Container Instances](https://docs.oracle.com/en-us/iaas/Content/container-instances/home.htm)
