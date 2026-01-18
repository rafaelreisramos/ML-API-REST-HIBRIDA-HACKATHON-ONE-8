# ==========================================
# 🚀 ChurnInsight - Auto Setup & Demo Script
# Equipe G8 - Hackathon Alura
# ==========================================

$ErrorActionPreference = "Stop"

function Print-Msg ($msg, $color="Cyan") {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $msg" -ForegroundColor $color
}

# 1. Verificar Pré-requisitos
Print-Msg "Verificando ambiente..."
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Print-Msg "❌ Docker não encontrado! Por favor, instale o Docker Desktop." "Red"
    exit 1
}
Print-Msg "✅ Docker detectado." "Green"

# 2. Configurar Diretório
$RepoUrl = "git@github.com:Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git"
$ProjectDir = "ML-API-REST-HIBRIDA-HACKATHON-ONE-8"

if (Test-Path "pom.xml") {
    Print-Msg "📂 Detectado execução dentro da pasta do projeto." "Yellow"
} else {
    if (-not (Test-Path $ProjectDir)) {
        Print-Msg "📥 Clonando repositório oficial..."
        try {
            git clone $RepoUrl
        } catch {
            Print-Msg "❌ Falha ao clonar via SSH. Tentando HTTPS..." "Yellow"
            git clone "https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git"
        }
    } else {
        Print-Msg "📂 Pasta do projeto já existe." "Yellow"
    }
    Set-Location $ProjectDir
}

# 3. Docker Compose (Build & Run)
Print-Msg "🏗️ Construindo e iniciando containers (Isso pode levar alguns minutos)..."
docker-compose down # Limpa estado anterior para garantir
docker-compose up -d --build

# 4. Aguardar Backend (Healthcheck)
Print-Msg "⏳ Aguardando inicialização da API (Porta 9999)..."
$BackendUrl = "http://localhost:9999/actuator/health"
$MaxRetries = 60 # 5 minutos max (h2 + postgres + build pode demorar)
$RetryCount = 0
$BackendUp = $false

while (-not $BackendUp -and $RetryCount -lt $MaxRetries) {
    Start-Sleep -Seconds 5
    try {
        $resp = Invoke-WebRequest -Uri $BackendUrl -UseBasicParsing -ErrorAction SilentlyContinue
        if ($resp.StatusCode -eq 200) { $BackendUp = $true }
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
    $RetryCount++
}

Write-Host "" # Quebra de linha

if (-not $BackendUp) {
    Print-Msg "❌ O Backend não respondeu a tempo. Verificando logs..." "Red"
    docker logs backend-api
    exit 1
}
Print-Msg "✅ Backend está ONLINE e SAUDÁVEL!" "Green"

# 5. Executar Testes Automatizados
Print-Msg "🧪 Executando bateria de testes E2E..." "Magenta"
if (Test-Path "run_all_tests.ps1") {
    powershell -ExecutionPolicy Bypass -File .\run_all_tests.ps1
} else {
    Print-Msg "⚠️ Script de testes não encontrado." "Yellow"
}

# 6. Abrir Navegador
Print-Msg "🌐 Inicializando Interface Web..."
Start-Process "http://localhost:3000"

Print-Msg "==================================================" "Green"
Print-Msg "✨ AMBIENTE PRONTO PARA DEMONSTRAÇÃO! ✨" "Green"
Print-Msg "Frontend: http://localhost:3000" "White"
Print-Msg "API:      http://localhost:9999" "White"
Print-Msg "Login:    admin / 123" "White"
Print-Msg "==================================================" "Green"
