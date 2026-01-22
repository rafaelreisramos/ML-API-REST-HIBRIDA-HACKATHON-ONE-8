# ============================================================================
# Script PowerShell para Atualização Remota do AI Service na OCI
# ============================================================================
# Este script conecta via SSH na VM OCI e executa a atualização segura
# ============================================================================

param(
    [switch]$DryRun = $false,
    [switch]$SkipBackup = $false
)

$ErrorActionPreference = "Stop"

# Cores para output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Log($message) {
    Write-ColorOutput Green "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $message"
}

function Warn($message) {
    Write-ColorOutput Yellow "[AVISO] $message"
}

function Error($message) {
    Write-ColorOutput Red "[ERRO] $message"
}

Write-Host ""
Write-Host "🚀 =============================================="
Write-Host "   Atualização Remota do AI Service - OCI"
Write-Host "   ChurnInsight - Equipe G8"
Write-Host "=============================================="
Write-Host ""

# ============================================================================
# ETAPA 1: Carregar Configuração
# ============================================================================

Log "Carregando configuração..."

$configPath = Join-Path $PSScriptRoot "config.bat"

if (-not (Test-Path $configPath)) {
    Error "Arquivo config.bat não encontrado!"
    Error "Copie config.bat.example para config.bat e configure."
    exit 1
}

# Ler variáveis do config.bat
$config = @{}
Get-Content $configPath | ForEach-Object {
    if ($_ -match '^set\s+"?([^=]+)"?=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim('"')
        $config[$key] = $value
    }
}

$instanceOcid = $config['INSTANCE_OCID']
$sshKeyPath = $config['SSH_KEY_PATH']
$sshUser = $config['SSH_USER']

if (-not $instanceOcid -or -not $sshKeyPath -or -not $sshUser) {
    Error "Configuração incompleta em config.bat"
    Error "Necessário: INSTANCE_OCID, SSH_KEY_PATH, SSH_USER"
    exit 1
}

# Expandir variáveis de ambiente no caminho da chave
$sshKeyPath = [System.Environment]::ExpandEnvironmentVariables($sshKeyPath)

if (-not (Test-Path $sshKeyPath)) {
    Error "Chave SSH não encontrada: $sshKeyPath"
    exit 1
}

Log "✅ Configuração carregada"
Write-Host ""

# ============================================================================
# ETAPA 2: Obter IP Público da Instância
# ============================================================================

Log "Obtendo IP público da instância OCI..."

try {
    $instanceInfo = oci compute instance get --instance-id $instanceOcid --query 'data' 2>$null | ConvertFrom-Json
    
    if ($instanceInfo.'lifecycle-state' -ne 'RUNNING') {
        Error "Instância não está rodando! Estado: $($instanceInfo.'lifecycle-state')"
        Error "Inicie a instância primeiro usando CONTROLE_OCI.bat"
        exit 1
    }
    
    # Obter VNIC attachment
    $vnicAttachment = oci compute vnic-attachment list `
        --compartment-id $instanceInfo.'compartment-id' `
        --instance-id $instanceOcid `
        --query 'data[0]."vnic-id"' `
        --raw-output 2>$null
    
    # Obter IP público
    $publicIp = oci network vnic get --vnic-id $vnicAttachment `
        --query 'data."public-ip"' `
        --raw-output 2>$null
    
    if (-not $publicIp) {
        Error "Não foi possível obter o IP público da instância"
        exit 1
    }
    
    Log "✅ IP Público: $publicIp"
    
}
catch {
    Error "Falha ao consultar OCI: $_"
    exit 1
}

Write-Host ""

# ============================================================================
# ETAPA 3: Verificar Conectividade SSH
# ============================================================================

Log "Verificando conectividade SSH..."

$sshTest = ssh -i $sshKeyPath -o ConnectTimeout=10 -o StrictHostKeyChecking=no `
    "$sshUser@$publicIp" "echo 'OK'" 2>&1

if ($LASTEXITCODE -ne 0) {
    Error "Falha ao conectar via SSH"
    Error "Verifique se a chave está correta e se a VM está acessível"
    exit 1
}

Log "✅ Conectividade SSH OK"
Write-Host ""

# ============================================================================
# ETAPA 4: Verificar Estado Atual do Sistema
# ============================================================================

Log "Verificando estado atual do sistema remoto..."

$healthCheck = ssh -i $sshKeyPath -o StrictHostKeyChecking=no `
    "$sshUser@$publicIp" @"
cd ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8 2>/dev/null || cd /opt/churninsight 2>/dev/null || { echo 'DIR_NOT_FOUND'; exit 1; }
docker-compose ps --format json 2>/dev/null || echo 'DOCKER_ERROR'
"@

if ($healthCheck -match 'DIR_NOT_FOUND') {
    Error "Diretório do projeto não encontrado na VM"
    Error "Esperado: ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8 ou /opt/churninsight"
    exit 1
}

if ($healthCheck -match 'DOCKER_ERROR') {
    Warn "Docker pode não estar rodando ou docker-compose não está instalado"
}

Log "✅ Sistema remoto acessível"
Write-Host ""

# ============================================================================
# ETAPA 5: Transferir Script de Atualização
# ============================================================================

Log "Transferindo script de atualização para VM..."

$localScriptPath = Join-Path $PSScriptRoot "update_ai_service_safe.sh"

if (-not (Test-Path $localScriptPath)) {
    Error "Script update_ai_service_safe.sh não encontrado!"
    exit 1
}

# Transferir via SCP
scp -i $sshKeyPath -o StrictHostKeyChecking=no `
    $localScriptPath "$sshUser@${publicIp}:/tmp/update_ai_service.sh" 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Error "Falha ao transferir script via SCP"
    exit 1
}

Log "✅ Script transferido"
Write-Host ""

# ============================================================================
# ETAPA 6: Executar Atualização Remota
# ============================================================================

if ($DryRun) {
    Warn "Modo DRY RUN ativado - Não executará a atualização"
    Log "Comandos que seriam executados:"
    Write-Host "  ssh $sshUser@$publicIp 'cd projeto && bash /tmp/update_ai_service.sh'"
    exit 0
}

Log "Executando atualização remota..."
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "  INÍCIO DA EXECUÇÃO REMOTA"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""

# Executar script remotamente
ssh -i $sshKeyPath -o StrictHostKeyChecking=no -t "$sshUser@$publicIp" @"
# Encontrar diretório do projeto
if [ -d ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8 ]; then
    cd ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8
elif [ -d /opt/churninsight ]; then
    cd /opt/churninsight
else
    echo "Diretório do projeto não encontrado!"
    exit 1
fi

# Dar permissão de execução e rodar script
chmod +x /tmp/update_ai_service.sh
bash /tmp/update_ai_service.sh
"@

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "  FIM DA EXECUÇÃO REMOTA"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""

if ($exitCode -ne 0) {
    Error "Atualização falhou com código de saída: $exitCode"
    Error "Verifique os logs acima para detalhes"
    exit $exitCode
}

# ============================================================================
# ETAPA 7: Verificação Pós-Atualização
# ============================================================================

Log "Verificando sistema após atualização..."

Start-Sleep -Seconds 5

# Testar endpoint público
try {
    $response = Invoke-WebRequest -Uri "http://${publicIp}:9999/actuator/health" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Log "✅ Backend está respondendo"
    }
}
catch {
    Warn "Backend pode não estar acessível externamente (firewall?)"
}

Write-Host ""

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================

Write-Host "🎉 =============================================="
Write-Host "   ATUALIZAÇÃO REMOTA CONCLUÍDA!"
Write-Host "=============================================="
Write-Host ""
Write-Host "📝 Informações:"
Write-Host ""
Write-Host "  • IP da VM: $publicIp"
Write-Host "  • Usuário SSH: $sshUser"
Write-Host "  • Status: Atualização executada com sucesso"
Write-Host ""
Write-Host "🔍 Próximos Passos:"
Write-Host ""
Write-Host "  1. Testar aplicação: http://${publicIp}:9999"
Write-Host "  2. Verificar logs remotos:"
Write-Host "     ssh -i $sshKeyPath $sshUser@$publicIp"
Write-Host "     cd ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8"
Write-Host "     docker-compose logs -f ai-service"
Write-Host ""
Write-Host "  3. Testar previsão via frontend"
Write-Host ""
Write-Host "✅ Sistema atualizado e operacional na OCI!"
Write-Host "=============================================="
Write-Host ""
