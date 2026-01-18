# 🔒 Configuração HTTPS com Traefik e Let's Encrypt

## Visão Geral

O ChurnInsight implementa HTTPS automático em produção usando:

- **Traefik v2.10**: Reverse proxy moderno e dinâmico
- **Let's Encrypt**: Certificados SSL gratuitos e válidos
- **nip.io**: Serviço de DNS wildcard para IPs públicos

## Arquitetura de Segurança

```
Internet (HTTPS:443)
    ↓
Traefik Proxy
    ├─ SSL/TLS Termination
    ├─ Let's Encrypt ACME Client
    └─ HTTP Redirect (80 → 443)
    ↓
Frontend (HTTP:80 interno)
```

## Como Funciona

### 1. Domínio Dinâmico (nip.io)

O serviço `nip.io` resolve automaticamente qualquer subdomínio para o IP incluído no nome:

```
137.131.179.58.nip.io → 137.131.179.58
```

Isso permite:

- ✅ Certificados SSL válidos sem comprar domínio
- ✅ Funciona com qualquer IP público
- ✅ Sem configuração de DNS necessária

### 2. Traefik Configuration

O Traefik é configurado via `docker-compose.yml`:

```yaml
traefik:
  image: traefik:v2.10
  command:
    - "--providers.docker=true"
    - "--entrypoints.web.address=:80"
    - "--entrypoints.websecure.address=:443"
    - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
    - "--certificatesresolvers.myresolver.acme.email=admin@${DOMAIN}"
    - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - "./letsencrypt:/letsencrypt"
    - "/var/run/docker.sock:/var/run/docker.sock:ro"
```

### 3. Frontend Labels

O frontend é exposto via Traefik usando labels Docker:

```yaml
frontend:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
    - "traefik.http.routers.frontend.entrypoints=websecure"
    - "traefik.http.routers.frontend.tls.certresolver=myresolver"
    - "traefik.http.routers.frontend-http.middlewares=redirect-to-https"
```

### 4. Certificado SSL

O certificado é:

- **Gerado automaticamente** na primeira requisição HTTPS
- **Armazenado** em `letsencrypt/acme.json`
- **Renovado automaticamente** antes de expirar (90 dias)
- **Válido** para navegadores modernos (Let's Encrypt é confiável)

## Deploy em Produção

### Pré-requisitos

- VM com IP público
- Portas 80 e 443 abertas no firewall
- Docker e Docker Compose instalados

### Passos de Deploy

#### 1. Configurar Variável de Ambiente

O script `setup_https.sh` detecta automaticamente o IP público:

```bash
#!/bin/bash
PUBLIC_IP=$(curl -s ifconfig.me)
echo "DOMAIN=$PUBLIC_IP.nip.io" > .env
```

#### 2. Iniciar Containers

```bash
docker-compose up -d
```

O Traefik irá:

1. Detectar o domínio via variável `${DOMAIN}`
2. Solicitar certificado ao Let's Encrypt
3. Validar via HTTP Challenge (porta 80)
4. Armazenar certificado em `acme.json`
5. Começar a servir HTTPS

#### 3. Verificar Status

```bash
# Ver logs do Traefik
docker logs traefik

# Testar HTTPS
curl -I https://<SEU_IP>.nip.io
```

## Configuração OCI (Oracle Cloud)

### Cloud-Init Automático

O arquivo `cloud-init-app.yaml` configura HTTPS automaticamente na criação da VM:

```yaml
runcmd:
  # Preparar Traefik
  - mkdir -p /opt/churninsight/letsencrypt
  - touch /opt/churninsight/letsencrypt/acme.json
  - chmod 600 /opt/churninsight/letsencrypt/acme.json
  
  # Detectar IP e configurar domínio
  - export PUBLIC_IP=$(curl -s ifconfig.me)
  - echo "DOMAIN=$PUBLIC_IP.nip.io" > /opt/churninsight/.env
  
  # Iniciar aplicação
  - docker-compose up -d --build
```

### Firewall OCI

As regras de segurança em `main.tf` incluem:

```hcl
# HTTP (para ACME Challenge)
ingress_security_rules {
  protocol = "6"
  source   = "0.0.0.0/0"
  tcp_options {
    min = 80
    max = 80
  }
}

# HTTPS
ingress_security_rules {
  protocol = "6"
  source   = "0.0.0.0/0"
  tcp_options {
    min = 443
    max = 443
  }
}
```

## Troubleshooting

### Certificado não gerado

**Sintoma**: Navegador mostra "Não Seguro" ou erro de certificado

**Causas comuns**:

1. Porta 80 bloqueada (Let's Encrypt precisa validar)
2. Domínio não resolve para o IP correto
3. Primeira requisição ainda em andamento

**Solução**:

```bash
# Verificar logs do Traefik
docker logs traefik 2>&1 | grep -i acme

# Verificar DNS
nslookup <SEU_IP>.nip.io

# Testar porta 80
curl http://<SEU_IP>.nip.io
```

### Redirecionamento não funciona

**Sintoma**: HTTP não redireciona para HTTPS

**Solução**:

```bash
# Verificar middleware de redirecionamento
docker exec traefik cat /etc/traefik/traefik.yml

# Testar manualmente
curl -I http://<SEU_IP>.nip.io
# Deve retornar: HTTP/1.1 307 Temporary Redirect
```

### Certificado expirado

**Sintoma**: Erro "Certificado expirado" após 90 dias

**Solução**:
O Traefik renova automaticamente. Se falhar:

```bash
# Remover certificado antigo
rm /opt/churninsight/letsencrypt/acme.json
touch /opt/churninsight/letsencrypt/acme.json
chmod 600 /opt/churninsight/letsencrypt/acme.json

# Reiniciar Traefik
docker-compose restart traefik
```

## Segurança Adicional

### Headers de Segurança

O Nginx (frontend) já inclui headers básicos:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

### Troubleshooting Comum

#### Login Travado / Timeout no Backend

Se o login funcionar rapidamente localmente mas travar na VM, especialmente ao usar criptografia (BCrypt, SSL, JWT), pode ser falta de entropia na VM Linux.
**Sintoma**: Logs param em "Started Application" e requisições de Login dão timeout.
**Solução**: Adicionar a opção Java para usar `/dev/urandom` (não bloqueante):

```yaml
environment:
  - JAVA_TOOL_OPTIONS=-Djava.security.egd=file:/dev/./urandom
```

Esta configuração já foi aplicada no `docker-compose.yml`.

#### Erro "Invalid CORS request" ou 403 Forbidden no Login

Ao acessar via HTTPS (domínio diferente da API interna), o navegador exige headers CORS. O Spring Security pode bloquear requisições antes mesmo delas chegarem ao Controller se a origem não for explicitamente permitida.
**Sintoma**: Login funciona via `curl` mas falha no navegador com erro de CORS ou 403.
**Solução**: Configurar CORS permissivo no Spring Security (`SecurityConfiguration.java`) para que ele sempre responda com `Access-Control-Allow-Origin: *`, independente de erros. A segurança é garantida pelo Token JWT, não pelo bloqueio de origem.

### Rate Limiting (Futuro)

Para produção de alta escala, considere adicionar ao Traefik:

```yaml
- "--http.middlewares.ratelimit.ratelimit.average=100"
- "--http.middlewares.ratelimit.ratelimit.burst=50"
```

## Monitoramento

### Dashboard do Traefik (Desenvolvimento)

Para habilitar o dashboard (apenas dev):

```yaml
traefik:
  command:
    - "--api.insecure=true"
  ports:
    - "8080:8080"
```

Acesse: `http://<IP>:8080/dashboard/`

### Logs de Acesso

```bash
# Ver últimas requisições
docker logs traefik --tail=100 -f

# Filtrar apenas HTTPS
docker logs traefik 2>&1 | grep "443"
```

## Referências

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Let's Encrypt](https://letsencrypt.org/)
- [nip.io](https://nip.io/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)

---

**Última atualização**: 2026-01-17
**Versão**: 1.0
