$timeoutSeconds = 300
$retryInterval = 5
$url = "http://localhost:9999/api/health"
$startTime = Get-Date

Write-Host "⏳ Aguardando API iniciar em $url..." -ForegroundColor Cyan

while ($true) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ API Disponível!" -ForegroundColor Green
            break
        }
    } catch {
        # Ignore errors and retry
    }

    if ((Get-Date) - $startTime -gt (New-TimeSpan -Seconds $timeoutSeconds)) {
        Write-Host "❌ Timeout aguardando API ($timeoutSeconds s)" -ForegroundColor Red
        Write-Host "Verifique o log da API para detalhes."
        exit 1
    }

    Start-Sleep -Seconds $retryInterval
    Write-Host "." -NoNewline
}

Write-Host ""
Write-Host "🚀 Iniciando testes E2E..." -ForegroundColor Cyan
& ".\run_all_tests.ps1"
