# 🆓 OCI Always Free Tier - Limites e Recursos

## 📊 Recursos Always Free Utilizados

Este projeto foi configurado para usar **APENAS** recursos do OCI Always Free Tier, garantindo custo zero permanente.

### ✅ Compute (Máquinas Virtuais)

- **2x VM.Standard.E2.1.Micro**
  - 1 OCPU (AMD EPYC 7551)
  - 1 GB RAM
  - **Uso no projeto:**
    - VM 1: Frontend + Backend (All-in-One)
    - VM 2: AI Service

### ✅ Block Storage

- **100 GB total** (gratuito permanente)
  - **Uso no projeto:** 10 GB para dados da aplicação

### ✅ Object Storage

- **20 GB** (gratuito permanente)
  - **Uso no projeto:** Logs e backups (opcional)

### ✅ Networking

- **1x VCN** (Virtual Cloud Network)
- **2x Public IPs**
- **10 TB de tráfego de saída/mês**

### ✅ Databases (Não utilizado neste projeto)

- **2x Oracle Autonomous Databases** (20 GB cada)
  - Disponível mas não necessário (usamos H2 in-memory)

## 🚫 Recursos NÃO Gratuitos (Evitados)

- ❌ Load Balancer (US$ 0.0225/hora)
- ❌ Container Instances (pago por uso)
- ❌ Kubernetes (OKE) (pago)
- ❌ VMs maiores que E2.1.Micro
- ❌ Block Storage > 100 GB

## 🏗️ Arquitetura Always Free

```
┌─────────────────────────────────────────────────┐
│           OCI Always Free Tier                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────┐   ┌──────────────────┐  │
│  │   VM 1 (E2.1)    │   │   VM 2 (E2.1)    │  │
│  │  ┌────────────┐  │   │  ┌────────────┐  │  │
│  │  │  Frontend  │  │   │  │ AI Service │  │  │
│  │  │   (Nginx)  │  │   │  │  (Docker)  │  │  │
│  │  └────────────┘  │   │  └────────────┘  │  │
│  │  ┌────────────┐  │   │                  │  │
│  │  │  Backend   │  │   │  Port: 5000      │  │
│  │  │  (Spring)  │  │   │  (Interno)       │  │
│  │  └────────────┘  │   │                  │  │
│  │                  │   │                  │  │
│  │  Ports: 80,9999  │   │                  │  │
│  │  Public IP       │   │  Public IP       │  │
│  └──────────────────┘   └──────────────────┘  │
│           │                       │            │
│           └───────────┬───────────┘            │
│                       │                        │
│              ┌────────▼────────┐               │
│              │   VCN (Free)    │               │
│              │  10.0.0.0/16    │               │
│              └─────────────────┘               │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 💰 Custo Mensal Estimado

**TOTAL: R$ 0,00** (Always Free)

## ⚠️ Limitações e Considerações

### Performance

- **CPU**: 1 OCPU por VM (adequado para demos e MVPs)
- **RAM**: 1 GB por VM (pode ser limitante para grandes volumes)
- **Recomendação**: Ideal para até 100 usuários simultâneos

### Escalabilidade

- **Horizontal**: Limitado a 2 VMs gratuitas
- **Vertical**: Não pode aumentar o shape sem custo
- **Solução**: Para produção com mais tráfego, migrar para shapes pagos

### Alta Disponibilidade

- **Sem Load Balancer**: Acesso direto ao IP da VM
- **Sem Auto-Scaling**: Capacidade fixa
- **Solução**: Usar DNS Round-Robin ou Cloudflare (gratuito)

## 🔧 Otimizações Aplicadas

1. **All-in-One VM**: Frontend + Backend na mesma VM economiza recursos
2. **Docker**: Isolamento sem overhead de VMs separadas
3. **H2 Database**: Banco em memória elimina necessidade de DB externo
4. **Nginx**: Servidor web leve e eficiente
5. **Cloud-init**: Provisionamento automático sem intervenção manual

## 📈 Quando Migrar para Recursos Pagos?

Considere upgrade se:

- ✅ Mais de 100 usuários simultâneos
- ✅ Necessidade de alta disponibilidade (99.9%+)
- ✅ Processamento de grandes volumes de dados (>10k predições/dia)
- ✅ Requisitos de compliance (ISO, SOC2, etc.)

## 🎯 Próximos Passos (Opcional)

### Free Tier + Cloudflare (Gratuito)

- CDN global
- DDoS protection
- SSL/TLS automático
- Load balancing entre as 2 VMs

### Upgrade Sugerido (Pago)

- Load Balancer: ~R$ 50/mês
- VMs maiores (E3.Flex): ~R$ 100/mês
- Autonomous Database: ~R$ 200/mês

## 📚 Referências

- [OCI Always Free Tier](https://www.oracle.com/cloud/free/)
- [OCI Pricing Calculator](https://www.oracle.com/cloud/costestimator.html)
- [OCI Free Tier FAQ](https://www.oracle.com/cloud/free/faq.html)
