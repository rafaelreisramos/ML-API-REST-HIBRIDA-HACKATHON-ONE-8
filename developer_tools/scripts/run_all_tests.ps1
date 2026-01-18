$ErrorActionPreference = "Stop"

Write-Host "Executando Todos os Testes E2E - ChurnInsight API" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gray
Write-Host ""

# Verificar se API está rodando
Write-Host "Verificando se API está rodando..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9999/actuator/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "API está UP e rodando!" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "ERRO: API nao está rodando em http://localhost:9999" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, inicie a API primeiro:" -ForegroundColor Yellow
    Write-Host "  1. Inicie o Docker Desktop" -ForegroundColor White
    Write-Host "  2. Execute: docker-compose up -d" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Lista de testes
$tests = @(
    @{Name = "test_api_e2e.py"; Description = "Fluxo completo com JWT + GraphQL" },
    @{Name = "test_validation.py"; Description = "Validacao de campos" },
    @{Name = "test_optimized_batch.py"; Description = "Processamento Otimizado (Batch)" }
)

$passed = 0
$failed = 0
$results = @()

foreach ($test in $tests) {
    $testName = $test.Name
    $testDesc = $test.Description
    
    Write-Host "Executando: $testName" -ForegroundColor Cyan
    Write-Host "   $testDesc" -ForegroundColor Gray
    Write-Host ""
    
    $startTime = Get-Date
    
    try {
        # Executa o python diretamente para capturar $LASTEXITCODE corretamente
        python $testName
        
        $duration = (Get-Date) - $startTime
        $totalSeconds = $duration.TotalSeconds
        $durationStr = "{0:N2}s" -f $totalSeconds

        # Verificando falhas
        if ($LASTEXITCODE -eq 0) {
            $passed++
            $status = "PASSOU"
            $color = "Green"
        }
        else {
            $failed++
            $status = "FALHOU"
            $color = "Red"
        }
        
        $results += @{
            Name        = $testName
            Status      = $status
            DurationStr = $durationStr
        }
        
        Write-Host ""
        Write-Host "$status em $durationStr" -ForegroundColor $color
        Write-Host "------------------------------------------------------------" -ForegroundColor Gray
        Write-Host ""
        
    }
    catch {
        $failed++
        $results += @{
            Name        = $testName
            Status      = "ERRO"
            DurationStr = "0s"
        }
        Write-Host "ERRO ao executar teste: $_" -ForegroundColor Red
        Write-Host "------------------------------------------------------------" -ForegroundColor Gray
        Write-Host ""
    }
}

# Resumo final
Write-Host ""
Write-Host "============================================================" -ForegroundColor Gray
Write-Host "RESUMO DOS TESTES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gray
Write-Host ""

foreach ($result in $results) {
    $rStatus = $result.Status
    $rName = $result.Name
    $rDur = $result.DurationStr
    
    Write-Host "  $rStatus $rName ($rDur)" -ForegroundColor White
}

Write-Host ""
Write-Host "Total de testes: $($tests.Count)" -ForegroundColor White
Write-Host "Passou: $passed" -ForegroundColor Green
Write-Host "Falhou: $failed" -ForegroundColor Red
Write-Host ""

if ($failed -eq 0) {
    Write-Host "TODOS OS TESTES PASSARAM COM SUCESSO!" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "Alguns testes falharam. Verifique os logs acima." -ForegroundColor Yellow
    exit 1
}
