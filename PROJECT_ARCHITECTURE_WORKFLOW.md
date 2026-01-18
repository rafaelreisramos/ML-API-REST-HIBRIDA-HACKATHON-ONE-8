# 🗺️ Arquitetura E2E & Workflow Visual - ChurnInsight

Este documento apresenta a infraestrutura completa, o pipeline de deployment e os fluxos de dados da aplicação **ChurnInsight** na Oracle Cloud Infrastructure (OCI).

> **Para Modelo NanoBanana**: Use os códigos Mermaid abaixo para gerar visualizações ricas da topologia.

## 🏗️ Topologia da Infraestrutura (Mermaid Graph)

Visão completa desde o usuário até a infraestrutura na nuvem.

```mermaid
%% Arquitetura E2E OCI ChurnInsight
graph TD
    %% Estilos
    classDef cloud fill:#f9f9f9,stroke:#333,stroke-width:2px,color:black;
    classDef compute fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:black;
    classDef container fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:black;
    classDef db fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,stroke-dasharray: 5 5,color:black;
    classDef actor fill:#eceff1,stroke:#455a64,stroke-width:2px,color:black;

    %% Atores Externos
    User((👤 Usuário)):::actor
    Dev((👨‍💻 Desenvolvedor)):::actor

    %% Infraestrutura OCI
    subgraph OCI_Cloud ["☁️ Oracle Cloud Infrastructure (OCI)"]
        direction TB
        
        %% Redes e Segurança
        subgraph VCN ["🔒 VCN (10.0.0.0/16)"]
            
            IGW[🌐 Internet Gateway]
            
            %% Instância Principal (Onde roda o Docker Compose)
            subgraph VM_Compute ["🖥️ VM App Server (OCI Instance 1)"]
                direction TB
                
                %% Camada de Borda (HTTPS)
                Traefik["🚦 Traefik Proxy<br/>(SSL/TLS Auto - nip.io)<br/>Port: 80/443"]:::container
                
                %% Camada de Aplicação (Docker Compose Network)
                subgraph Docker_Network ["🐳 Internal Docker Network"]
                    Frontend["⚛️ Frontend UI<br/>(React + Nginx)<br/>Port: 80"]:::container
                    
                    subgraph Backend_Cluster ["⚙️ Backend Services"]
                        ApiJava["☕ Backend API<br/>(Spring Boot 3)<br/>Port: 9999"]:::container
                        AiPython["🐍 AI Service<br/>(Flask + Scikit-Learn)<br/>Port: 5000"]:::container
                    end
                    
                    DB[(🗄️ PostgreSQL / H2<br/>Database)]:::db
                end
            end

            %% Instância Secundária (Provisionada pelo Terraform, mas containers não distribuídos ainda)
            subgraph VM_AI ["🖥️ VM AI Server (OCI Instance 2)"]
                AiStandalone["🐍 AI Service (Standby)<br/>Reserved for Scale-out"]:::compute
            end
        end
    end

    %% Pipeline DevOps
    subgraph Pipeline ["🚀 Deployment Pipeline"]
        Git[📂 GitHub Repo]
        Terraform[🏗️ Terraform]
        SSH[🔑 SSH Access]
    end

    %% Conexões de Deploy
    Dev -->|Commit/Push| Git
    Dev -->|Plan/Apply| Terraform
    Terraform -->|Provisiona| VCN
    Terraform -->|Configura| VM_Compute
    Git -->|Git Pull| VM_Compute
    Dev -->|SSH Connection| VM_Compute

    %% Conexões de Rede OCI
    User ==>|HTTPS Request| IGW
    IGW ==>|Route Table| Traefik

    %% Roteamento Interno Traefik
    Traefik -->|Host: *.nip.io| Frontend
    Traefik -->|/api/* OR /login| ApiJava

    %% Fluxo de Dados Aplicação
    Frontend -.->|Fetch API| Traefik
    ApiJava <-->|JPA| DB
    ApiJava <-->|HTTP Predição| AiPython

    %% Classes
    class OCI_Cloud cloud;
    class VM_Compute compute;
```

---

## 🔄 Fluxo de Negócio E2E: Análise de Churn (Sequence Diagram)

Detalhamento de como um arquivo CSV se transforma em insights de negócio.

```mermaid
sequenceDiagram
    autonumber
    
    actor U as 👤 Usuário
    participant P as 🚦 Traefik (Proxy)
    participant F as ⚛️ Frontend (React)
    participant B as ☕ Backend (Spring Security)
    participant A as 🐍 AI Service (Python)
    participant D as 🗄️ Database

    box rgb(240, 248, 255) "Autenticação"
    U->>P: Acessa https://...nip.io
    P->>F: Serve Aplicação React
    U->>F: Preenche Login (admin/123456)
    F->>P: POST /login
    P->>B: Encaminha Requisição
    B->>B: Valida Credenciais (Spring Security)
    B-->>F: Retorna Token JWT (200 OK)
    end

    box rgb(255, 248, 240) "Processamento Batch (E2E)"
    U->>F: Upload CSV Clientes
    F->>P: POST /api/churn/upload (Multipart)
    P->>B: Encaminha com Token
    B->>B: Valida Token & Parse CSV
    B->>D: Salva Dados Brutos (Transacional)
    
    par Processamento Assíncrono / Rápido
        B->>A: POST /predict (Lista de Clientes)
        Note right of A: Modelo Random Forest<br/>Calcula Probabilidade
        A-->>B: Retorna [Score, Classe]
    end
    
    B->>D: Atualiza Clientes com Score de Churn
    B-->>F: Retorna JSON (Status Processamento)
    end

    box rgb(240, 255, 240) "Visualização"
    F->>P: GET /api/dashboard/metrics
    P->>B: Request Métricas
    B->>D: Query SQL (Agregação)
    D-->>B: Dados Consolidados
    B-->>F: JSON Métricas
    F-->>U: Renderiza Gráficos & KPIs
    end
```

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Função |
| :--- | :--- | :--- |
| **Infra OCI** | Terraform | Código para criar VCN, Security Lists, VM |
| **Proxy** | Traefik | SSL Automático (Let's Encrypt), Roteamento |
| **Frontend** | React + Vite | Interface do Usuário, Dashboard |
| **Backend** | Spring Boot 3 | API REST, Segurança (JWT), Orquestração |
| **IA/ML** | Python (Flask) | Modelo Preditivo, Scikit-Learn |
| **Dados** | PostgreSQL | Persistência Relacional |
| **OS** | Oracle Linux 8 | Sistema Operacional da VM |

---
*Gerado para documentação visual do projeto ChurnInsight.*
