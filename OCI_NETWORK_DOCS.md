# 🌐 Arquitetura de Rede OCI (Terraform) - ChurnInsight

Este documento detalha a infraestrutura de rede provisionada automaticamente via Terraform na Oracle Cloud Infrastructure (OCI). A arquitetura foi desenhada para suportar uma aplicação híbrida com Frontend, Backend Java e Serviço de IA Python, garantindo performance e controle de acesso.

## 📐 Topologia Geral

A topologia utiliza uma **Virtual Cloud Network (VCN)** única com uma **Subnet Pública** para hospedar todos os serviços, simplificando a comunicação inicial e aproveitando IPs públicos de alta velocidade para acesso e manutenção.

```mermaid
graph TD
    Internet((Internet)) --> IGW[Internet Gateway]
    IGW --> RouteTable[Route Table Public]
    RouteTable --> SubnetPublic[Subnet Pública: 10.0.1.0/24]
    
    subgraph VCN [VCN: 10.0.0.0/16]
        subgraph SubnetPublic
            AppServer[App Server<br/>(Front + Back)<br/>IP: Public]
            AIServer[AI Server<br/>(Python ML)<br/>IP: Public]
        end
        
        AppServer -- HTTP :5000 --> AIServer
    end

    User(Usuário) -- HTTP :80 --> AppServer
    User -- HTTPS :443 --> AppServer
    User -- API :9999 --> AppServer
    Admin(Admin) -- SSH :22 --> AppServer
    Admin -- SSH :22 --> AIServer
```

---

## 🛠️ Detalhes dos Componentes

### 1. Virtual Cloud Network (VCN)

A rede principal que isola logicamente a infraestrutura na nuvem.

- **CIDR Block**: `10.0.0.0/16` (65.536 IPs)
- **Nome DNS**: `churninsightvcn`
- **Compartment**: Hackathon_One

### 2. Subnet Pública

Sub-rede onde as instâncias de computação são provisionadas. Permite atribuição de IPs públicos.

- **CIDR Block**: `10.0.1.0/24` (256 IPs)
- **Acesso**: Público (Internet Gateway)
- **DNS Label**: `public`

### 3. Roteamento (Route Table)

Define como o tráfego flui para fora da subnet.

- **Rota Padrão**: Destino `0.0.0.0/0` -> Alvo `Internet Gateway` (Permite acesso à internet para updates e respostas a requisições).

---

## 🛡️ Segurança de Rede (Security Lists)

As regras de firewall são aplicadas no nível da sub-rede via **Security Lists**. O princípio utilizado foi "Liberar apenas o essencial".

### Regras de Entrada (Ingress)

| Porta | Protocolo | Origem | Descrição |
| :--- | :--- | :--- | :--- |
| **22** | TCP | `0.0.0.0/0` (Any) | Acesso SSH para administração remota. |
| **80** | TCP | `0.0.0.0/0` (Any) | Acesso HTTP ao Frontend (Web Dashboard). |
| **443** | TCP | `0.0.0.0/0` (Any) | Acesso HTTPS (Futuro). |
| **9999** | TCP | `0.0.0.0/0` (Any) | Acesso à API Backend (GraphQL). |
| **5000** | TCP | `10.0.0.0/16` (VCN) | **Acesso Interno** ao Serviço de IA. Restrito à rede interna. |

### Regras de Saída (Egress)

| Destino | Protocolo | Descrição |
| :--- | :--- | :--- |
| `0.0.0.0/0` | All | Permite saída irrestrita (necessário para `yum update`, `git pull`, etc). |

---

## 🔌 Conectividade entre Serviços

1. **Frontend -> Backend**:
    - Comunicação local (localhost) ou via IP Público na porta `9999` (se containerizado, usam a rede Docker, mas a porta 9999 exposta permite acesso externo).

2. **Backend -> AI Service**:
    - O Backend Java comunica-se com o AI Service via HTTP.
    - O acesso deve ser feito pelo **IP Privado** do AI Service na porta `5000`.
    - IP Privado típico: `10.0.1.x`.

---

## 📝 Como modificar

Toda a definição de rede está codificada no arquivo `oci-pipeline/terraform/main.tf`.

Para adicionar uma nova porta (ex: Banco de Dados na 5432):

1. Edite `main.tf`.
2. Adicione um bloco `ingress_security_rules` no recurso `oci_core_security_list.public`.
3. Execute `terraform apply`.

```hcl
ingress_security_rules {
  protocol    = "6" # TCP
  source      = "0.0.0.0/0"
  tcp_options {
    min = 5432
    max = 5432
  }
}
```
