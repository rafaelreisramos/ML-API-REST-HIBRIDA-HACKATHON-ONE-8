# 🎮 OCI VM Control Center

Bem-vindo ao **OCI VM Control Center**, uma suíte de ferramentas desenvolvida pela **Equipe G8** para facilitar o gerenciamento, operação e diagnóstico da infraestrutura ChurnInsight na Oracle Cloud Infrastructure (OCI).

Este diretório contém scripts automatizados para controlar o ciclo de vida da instância (Start/Stop), realizar acessos seguros (SSH) e diagnósticos de rede sem a necessidade de memorizar comandos complexos da OCI CLI.

---

## 🚀 Funcionalidades

O script principal `CONTROLE_OCI.bat` oferece um menu interativo com as seguintes capacidades:

1. **Start Instance**: Inicia a VM de produção na OCI.
2. **Stop Instance**: Realiza um desligamento suave (Soft Stop) para economizar recursos.
3. **Health Check**: Verifica o status atual (RUNNING, STOPPED) e recupera dinamicamente o **IP Público**.
4. **Auto SSH**: Conecta automaticamente via SSH à instância, resolvendo o IP e utilizando sua chave privada configurada, sem necessidade de digitar o comando `ssh` manualmente.
5. **Audit Logs**: Visualiza o histórico de operações realizadas pela ferramenta.

---

## 📋 Pré-requisitos

Para utilizar estas ferramentas, você precisa:

1. **OCI CLI Instalada**: A interface de linha de comando da Oracle deve estar instalada e configurada no seu Windows.
    * Teste rodando: `oci --version` no terminal.
2. **Configuração de Autenticação**: Você deve ter rodado `oci setup config` e ter um perfil funcional.
3. **Chave SSH**: A chave privada (`.key` ou sem extensão) correspondente à chave pública provisionada na VM.

---

## ⚙️ Configuração (Setup Inicial)

Antes de usar, é necessário configurar o ambiente:

1. **Crie o arquivo de configuração**:
    Copie o arquivo de exemplo `config.bat.example` e renomeie para `config.bat`.

    ```powershell
    copy config.bat.example config.bat
    ```

2. **Edite o `config.bat`**:
    Abra o arquivo em um editor de texto e preencha as variáveis obrigatórias:

    * `INSTANCE_OCID`: O ID único da sua instância OCI (Obtenha via Console OCI ou Terraform Output).
        > 💡 **Dica:** Os IPs e detalhes atuais da infraestrutura estão documentados em: [**OCI_ACCESS_INFO.md**](../docs/OCI_ACCESS_INFO.md).
    * `SSH_KEY_PATH`: Caminho absoluto para sua chave privada SSH (ex: `C:\Users\Voce\.ssh\id_rsa`).
    * `SSH_USER`: Usuário de login (Geralmente `opc` para Oracle Linux ou `ubuntu` para Ubuntu).

    **Exemplo:**

    ```bat
    set "INSTANCE_OCID=ocid1.instance.oc1.sa-saopaulo-1.abcdef12345..."
    set "SSH_KEY_PATH=%USERPROFILE%\.ssh\oci_key"
    ```

---

## 🕹️ Como Usar

Basta executar o script principal:

1. Abra a pasta no Explorador de Arquivos e clique duas vezes em `CONTROLE_OCI.bat`.
2. Ou execute via terminal:

    ```powershell
    .\CONTROLE_OCI.bat
    ```

3. Use o teclado numérico para selecionar a operação desejada.

---

## 🛠️ Ferramentas Auxiliares

### `diagnose_port_9999.sh`

Este é um script Shell (Linux) destinado a ser executado **DENTRO** da VM.
Ele serve para diagnosticar por que a aplicação Backend (Porta 9999) pode não estar respondendo.

**Uso:**

1. Conecte na VM (Opção 4 do menu).
2. Copie este script para lá ou cole seu conteúdo.
3. Execute: `bash diagnose_port_9999.sh`

### `run_diagnostics.ps1`

Script PowerShell para diagnósticos rápidos locais e verificações de dependências.

---

## ⚠️ Troubleshooting

**Erro: "OCI CLI not found"**

* Verifique se instalou a OCI CLI.
* Se instalou em um local customizado, edite o `config.bat` e defina `OCI_PATH`.

**Erro: "Authentication failed"**

* Sua sessão da OCI CLI pode ter expirado ou a chave de API é inválida. Tente rodar `oci setup repair` ou verifique suas chaves na Console OCI.

**Erro: "Permission Denied (publickey)" no SSH**

* Verifique se o caminho da chave em `config.bat` está correto.
* Certifique-se de que é a chave privada correta pareada com a VM atual.

---

*VibeCode Engineering - Hackathon Alura G8*
