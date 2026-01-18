$AppServerIP = "137.131.179.58"
$SSHKey = "C:\Users\renan\.ssh\id_ed25519"

Write-Host "Verificando status do App Server ($AppServerIP)..." -ForegroundColor Cyan

# Tenta conectar via SSH
try {
    $sshOutput = ssh -o StrictHostKeyChecking=no -i $SSHKey opc@$AppServerIP "tail -n 5 /var/log/cloud-init-output.log && sudo docker ps" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Conexão SSH bem sucedida!" -ForegroundColor Green
        Write-Host "--- Logs Recentes do Cloud-Init ---" -ForegroundColor Yellow
        Write-Host $sshOutput
        Write-Host "-----------------------------------" -ForegroundColor Yellow
    }
    else {
        if ($sshOutput -match "System is booting up") {
            Write-Host "⏳ Sistema ainda inicializando. Tente novamente em 1 minuto." -ForegroundColor Yellow
        }
        else {
            Write-Host "❌ Erro ao conectar: $sshOutput" -ForegroundColor Red
        }
    }
}
catch {
    Write-Host "❌ Falha na conexão." -ForegroundColor Red
}

Write-Host "`nTestando acesso WEB..." -ForegroundColor Cyan
try {
    $web = Invoke-WebRequest -Uri "http://$AppServerIP" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($web.StatusCode -eq 200) {
        Write-Host "✅ Frontend acessível via HTTP!" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Frontend respondeu com código: $($web.StatusCode)" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Frontend ainda não acessível via HTTP (pode estar subindo ou firewall configurando)." -ForegroundColor Red
}
