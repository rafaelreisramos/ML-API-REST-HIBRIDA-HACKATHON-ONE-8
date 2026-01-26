$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$OCI_URL = "http://137.131.179.58:9999"

Write-Host "Executando Testes E2E contra OCI - ($OCI_URL)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gray

# Verificar se API Remota está rodando
Write-Host "Verificando conectividade com OCI..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$OCI_URL/actuator/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "API OCI está acessível!" -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Não foi possível conectar na OCI ($OCI_URL)" -ForegroundColor Red
    exit 1
}

# Definir Variável de Ambiente para os scripts Python
$env:API_URL = $OCI_URL

# Lista de testes (usando mesmos nomes que run_all_tests.ps1)
# Removido testes de batch muito grandes para não onerar a rede no teste rápido
$tests = @(
    "oci_test_graphql.py",  # Nosso teste customizado de conectividade
    "test_api_e2e.py",      # Teste funcional completo
    "test_validation.py"    # Validações de campos
)

$passed = 0
$failed = 0

foreach ($test in $tests) {
    Write-Host "`nExecutando: $test" -ForegroundColor Cyan
    try {
        if (Test-Path $test) {
            python $test
            if ($LASTEXITCODE -eq 0) { $passed++ } else { $failed++ }
        }
        else {
            Write-Host "Script nao encontrado: $test" -ForegroundColor Red
            $failed++
        }
    }
    catch {
        Write-Host "Erro ao executar $test" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n============================================================" -ForegroundColor Gray
Write-Host "Total: $($tests.Count) | Passou: $passed | Falhou: $failed" -ForegroundColor White
if ($failed -eq 0) {
    Write-Host "SUCESSO TOTAL! OCI ESTÁ PRONTA!" -ForegroundColor Green
}
else {
    Write-Host "ALERTA: Alguns testes falharam." -ForegroundColor Red
}
