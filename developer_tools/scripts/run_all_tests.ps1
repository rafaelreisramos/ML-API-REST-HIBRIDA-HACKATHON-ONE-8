$ErrorActionPreference = "Stop"

# ============================================================================
# CHURN INSIGHT - E2E TEST RUNNER
# ============================================================================
# Uso: 
#   .\run_all_tests.ps1            -> Roda localmente (localhost:9999)
#   .\run_all_tests.ps1 -Target OCI -> Roda contra OCI (137.131.179.58)
#   .\run_all_tests.ps1 -Url "..."  -> Roda contra URL customizada
# ============================================================================

param (
    [string]$Target = "Local",
    [string]$Url = ""
)

# 1. Configurar URL do Ambiente
if ($Url) {
    $BASE_URL = $Url
}
elseif ($Target -eq "OCI") {
    $BASE_URL = "http://137.131.179.58:9999"
}
else {
    $BASE_URL = "http://localhost:9999"
}

$env:API_URL = $BASE_URL

Clear-Host
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  TEST DRIVER - CHURN INSIGHT API" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Target:  $Target" -ForegroundColor Yellow
Write-Host "URL:     $BASE_URL" -ForegroundColor Yellow
Write-Host "Date:    $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# 2. Health Check Prep
Write-Host "[0] Health Check (Pré-requisito)" -ForegroundColor Cyan
try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-WebRequest -Uri "$BASE_URL/actuator/health" -UseBasicParsing -TimeoutSec 5
    $sw.Stop()
    
    $ms = $sw.Elapsed.TotalMilliseconds.ToString('N0')
    Write-Host "  ✓ API Online ($ms ms)" -ForegroundColor Green
}
catch {
    Write-Host "  ✗ FALHA CRÍTICA: Não foi possível conectar em $BASE_URL" -ForegroundColor Red
    Write-Host "  Verifique se o serviço está rodando ou se o IP está correto." -ForegroundColor Red
    if ($Target -eq "Local") {
        Write-Host "  Dica: Execute 'docker-compose up -d'" -ForegroundColor Gray
    }
    exit 1
}

# 3. Definição da Suite de Testes
$testSuite = @(
    @{
        File = "oci_test_graphql.py"
        Name = "1. Conectividade & Schema"
        Desc = "Verifica login admin e introspecção GraphQL"
    },
    @{
        File = "test_api_e2e.py"
        Name = "2. Fluxo End-to-End"
        Desc = "Ciclo completo: Login -> Mutation (Criar) -> Query (Ler)"
    },
    @{
        File = "verify_model_logic.py"
        Name = "3. Regras de Negócio"
        Desc = "Verifica se o cálculo de churn segue a lógica esperada"
    },
    @{
        File = "test_validation.py"
        Name = "4. Validação de Segurança"
        Desc = "Garante rejeição de dados inválidos/maliciosos"
    },
    @{
        File = "test_optimized_batch.py"
        Name = "5. Processamento em Lote"
        Desc = "Testa upload de CSV e fila de processamento"
    }
)

# 4. Execução dos Testes
$passed = 0
$failed = 0
$results = @()

Write-Host ""
Write-Host "Iniciando Execução da Suite de Testes..." -ForegroundColor Yellow
Write-Host "------------------------------------------------------------" -ForegroundColor Gray

foreach ($test in $testSuite) {
    $fname = $test.File
    $tname = $test.Name
    $tdesc = $test.Desc
    
    Write-Host "`n[$tname] $tdesc" -ForegroundColor Cyan
    
    if (Test-Path $fname) {
        $startTime = Get-Date
        
        try {
            # Executa o processo e espera terminar
            $process = Start-Process -FilePath "python" -ArgumentList "$fname" -NoNewWindow -PassThru -Wait
            $exitCode = $process.ExitCode
            
            $duration = (Get-Date) - $startTime
            $durStr = "{0:N2}s" -f $duration.TotalSeconds
            
            if ($exitCode -eq 0) {
                Write-Host "  ✓ PASSOU ($durStr)" -ForegroundColor Green
                $passed++
                $results += @{ Name=$tname; Status="PASS"; Time=$durStr }
            } else {
                Write-Host "  ✗ FALHOU ($durStr) - Exit Code: $exitCode" -ForegroundColor Red
                $failed++
                $results += @{ Name=$tname; Status="FAIL"; Time=$durStr }
            }
        } catch {
            Write-Host "  ✗ ERRO DE EXECUÇÃO: $_" -ForegroundColor Red
            $failed++
            $results += @{ Name=$tname; Status="ERROR"; Time="0s" }
        }
    } else {
        Write-Host "  ⚠ ARQUIVO NÃO ENCONTRADO: $fname" -ForegroundColor Yellow
        $failed++
        $results += @{ Name=$tname; Status="MISSING"; Time="0s" }
    }
}

# 5. Relatório Final
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RELATÓRIO DE EXECUÇÃO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($res in $results) {
    $color = "Green"
    if ($res.Status -ne "PASS") { $color = "Red" }
    
    Write-Host "  [$($res.Status)] $($res.Name) - $($res.Time)" -ForegroundColor $color
}

Write-Host ""
Write-Host "Total: $($testSuite.Count) | Passou: $passed | Falhou: $failed" -ForegroundColor White

if ($failed -eq 0) {
    Write-Host ""
    Write-Host "  🚀 SUCESSO TOTAL! APLICAÇÃO ESTÁ PRONTA!" -ForegroundColor Green
    Write-Host ""
    exit 0
} else {
    Write-Host ""
    Write-Host "  ⚠ ATENÇÃO: Verifique os erros acima." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
