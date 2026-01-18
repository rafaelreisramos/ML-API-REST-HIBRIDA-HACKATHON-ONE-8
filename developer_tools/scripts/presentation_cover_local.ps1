$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Clear-Host

# --- DETECTAR DIRETÓRIO RAIZ DO PROJETO ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

# --- CONFIGURAÇÃO FORÇADA PARA LOCALHOST ---
$env:API_URL = "http://localhost:9999"

# --- CORES ---
$White = [ConsoleColor]::White
$Green = [ConsoleColor]::Green
$Cyan = [ConsoleColor]::Cyan
$Yellow = [ConsoleColor]::Yellow
$Red = [ConsoleColor]::Red
$Blue = [ConsoleColor]::Blue
$Magenta = [ConsoleColor]::Magenta
$Gray = [ConsoleColor]::Gray
$DGray = [ConsoleColor]::DarkGray

# --- FUNÇÕES DE DESENHO ---
function Center-Text {
    param($Text, $Color = $White)
    try {
        $w = $Host.UI.RawUI.WindowSize.Width
    }
    catch {
        $w = 120 # Fallback
    }
    $pad = [Math]::Max(0, [Math]::Floor(($w - $Text.Length) / 2))
    Write-Host (" " * $pad) -NoNewline
    Write-Host $Text -ForegroundColor $Color
}

function Show-Enterprise-Dashboard {
    Clear-Host
    Write-Host "`n`n"
    
    # 1. HEADER LOGO (ASCII SEGURO)
    $header = @(
        "   _______  __ ____  ___________  __   INSIGHT     ",
        "  / ____/ |/ // __ \/ ____/   \ \/ /   AI-POWERED   ",
        " / /    |   // / / / /   / /| | \  /    CHURN       ",
        "/ /___ /   |/ /_/ / /___/ ___ | /  \    PREDICTION  ",
        "\____//_/|_/_____/\____/_/  |_|/_/\_\               "
    )
    foreach ($h in $header) { Center-Text $h $Cyan }
    
    Write-Host "`n"
    Center-Text "A R Q U I T E T U R A   H I B R I D A   ( A M B I E N T E   L O C A L )" $Yellow
    Write-Host "`n`n"

    # LAYOUT GRID
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|      LOCALHOST       |   |      TERRAFORM       |   |        DOCKER        |" $White
    Center-Text "|    (Dev/Test Env)    |   |    (Infra as Code)   |   |     (Containers)     |" $Red
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    
    Write-Host "`n"
    
    # Row 2
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|    SPRING BOOT 3     |   |      JPA / HIBER     |   |       GRAPHQL        |" $White
    Center-Text "|    (Microservice)    |   |     (Persistence)    |   |      (Data Mesh)     |" $Green
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray

    Write-Host "`n"

    # Row 3
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|      POSTGRESQL      |   |       TRAEFIK        |   |    ACTUATOR HEALTH   |" $White
    Center-Text "|  (Relational Data)   |   |   (Reverse Proxy)    |   |    (Observability)   |" $Blue
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray

    Write-Host "`n`n"
    Center-Text "STATUS DO SISTEMA: PRONTO PARA DEMONSTRACAO (LOCAL)" $Green
    Write-Host "`n`n`n"
    Center-Text "Pressione [ENTER] para iniciar a Demonstracao Local..." $Gray
    Read-Host
    
    # Iniciar o Orquestrador Python HERDANDO a variavel API_URL local
    Push-Location $ProjectRoot
    $env:PYTHONIOENCODING = 'utf-8'
    Start-Process python -ArgumentList "$ProjectRoot\developer_tools\scripts\orquestrador.py" -NoNewWindow -Wait
    Pop-Location
}

Show-Enterprise-Dashboard
