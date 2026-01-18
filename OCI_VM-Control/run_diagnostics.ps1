# ============================================================================
# Script de Diagnóstico Remoto - Porta 9999
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  DIAGNÓSTICO DE CONECTIVIDADE - PORTA 9999 (GraphQL)" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Carregar configuração
if (-not (Test-Path ".\config.bat")) {
    Write-Host "[ERRO] Arquivo config.bat não encontrado!" -ForegroundColor Red
    exit 1
}

# Ler variáveis do config.bat
$configContent = Get-Content ".\config.bat"
$INSTANCE_OCID = ($configContent | Select-String "set INSTANCE_OCID=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value }).Trim()
$SSH_USER = ($configContent | Select-String "set SSH_USER=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value }).Trim()
$SSH_KEY_PATH = ($configContent | Select-String "set SSH_KEY_PATH=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value }).Trim()
$OCI_PATH_CONFIG = ($configContent | Select-String "set OCI_PATH=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value }).Trim()

if ($OCI_PATH_CONFIG) {
    $OCI_EXE = Join-Path $OCI_PATH_CONFIG "oci.exe"
}
else {
    $OCI_EXE = "oci"
}

Write-Host "[1/4] Obtendo IP público da VM..." -ForegroundColor Yellow

# Obter IP público
try {
    $PUBLIC_IP = & $OCI_EXE compute instance list-vnics --instance-id $INSTANCE_OCID --query 'data[0]."public-ip"' --raw-output --auth security_token 2>$null
    
    if ([string]::IsNullOrWhiteSpace($PUBLIC_IP)) {
        Write-Host "[ERRO] Não foi possível obter o IP público" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  ✓ IP Público: $PUBLIC_IP" -ForegroundColor Green
}
catch {
    Write-Host "[ERRO] Falha ao executar OCI CLI: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/4] Copiando script de diagnóstico para a VM..." -ForegroundColor Yellow

# Copiar script para a VM
try {
    scp -o StrictHostKeyChecking=no -i "$SSH_KEY_PATH" ".\diagnose_port_9999.sh" "${SSH_USER}@${PUBLIC_IP}:/tmp/" 2>$null
    Write-Host "  ✓ Script copiado com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "[ERRO] Falha ao copiar script: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/4] Executando diagnóstico na VM..." -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Executar diagnóstico
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY_PATH" "${SSH_USER}@${PUBLIC_IP}" 'chmod +x /tmp/diagnose_port_9999.sh; /tmp/diagnose_port_9999.sh'

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "[4/4] Testando conectividade externa (do seu computador)..." -ForegroundColor Yellow
Write-Host ""

# Testar do computador local
try {
    $response = Invoke-WebRequest -Uri "http://${PUBLIC_IP}:9999/actuator/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "  ✓ Conectividade EXTERNA OK - HTTP $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  URL: http://${PUBLIC_IP}:9999/actuator/health" -ForegroundColor Cyan
}
catch {
    if ($_.Exception.Response.StatusCode) {
        Write-Host "  ⚠ Servidor respondeu com HTTP $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
    else {
        Write-Host "  ✗ NÃO foi possível conectar externamente" -ForegroundColor Red
        Write-Host "  Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  TESTE COMPLETO" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URLs para teste:" -ForegroundColor White
Write-Host "  Health Check: http://${PUBLIC_IP}:9999/actuator/health" -ForegroundColor Cyan
Write-Host "  GraphQL:      http://${PUBLIC_IP}:9999/graphql" -ForegroundColor Cyan
Write-Host "  Login:        http://${PUBLIC_IP}:9999/login" -ForegroundColor Cyan
Write-Host ""
