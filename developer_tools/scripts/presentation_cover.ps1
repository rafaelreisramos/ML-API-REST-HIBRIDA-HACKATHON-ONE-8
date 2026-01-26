$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Clear-Host

# --- CORES ---
$White  = [ConsoleColor]::White
$Green  = [ConsoleColor]::Green
$Cyan   = [ConsoleColor]::Cyan
$Yellow = [ConsoleColor]::Yellow
$Red    = [ConsoleColor]::Red
$Blue   = [ConsoleColor]::Blue
$Magenta= [ConsoleColor]::Magenta
$Gray   = [ConsoleColor]::Gray
$DGray  = [ConsoleColor]::DarkGray

# --- FUNÇÕES DE DESENHO ---
function Center-Text {
    param($Text, $Color=$White)
    try {
        $w = $Host.UI.RawUI.WindowSize.Width
    } catch {
        $w = 120 # Fallback se não detectar largura
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
    foreach($h in $header) { Center-Text $h $Cyan }
    
    Write-Host "`n"
    Center-Text "A R Q U I T E T U R A   H I B R I D A   &   S C A L A B L E" $Yellow
    Write-Host "`n`n"

    # LAYOUT GRID (ASCII Simples e Seguro)
    # Row 1: INFRA & DEVOPS
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|      ORACLE OCI      |   |      TERRAFORM       |   |        DOCKER        |" $White
    Center-Text "|     (Cloud Infra)    |   |    (Infra as Code)   |   |     (Containers)     |" $Red
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    
    Write-Host "`n"
    
    # Row 2: BACKEND CORE
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|    SPRING BOOT 3     |   |      JPA / HIBER     |   |       GRAPHQL        |" $White
    Center-Text "|    (Microservice)    |   |     (Persistence)    |   |      (Data Mesh)     |" $Green
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray

    Write-Host "`n"

    # Row 3: DATA & TRAFFIC
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray
    Center-Text "|      POSTGRESQL      |   |       TRAEFIK        |   |    ACTUATOR HEALTH   |" $White
    Center-Text "|  (Relational Data)   |   |   (Reverse Proxy)    |   |    (Observability)   |" $Blue
    Center-Text "+----------------------+   +----------------------+   +----------------------+" $DGray

    Write-Host "`n`n"
    Center-Text "STATUS DO SISTEMA: PRONTO PARA DEMONSTRACAO" $Green
    Write-Host "`n`n`n"
    Center-Text "Pressione [ENTER] para iniciar a Demonstracao..." $Gray
    Read-Host
    
    # Iniciar o Orquestrador Python
    Start-Process python -ArgumentList "developer_tools/scripts/orquestrador.py" -NoNewWindow -Wait
}

Show-Enterprise-Dashboard
