@echo off
:: Script simplificado para diagnóstico da porta 9999

echo ============================================================================
echo   DIAGNOSTICO DE CONECTIVIDADE - PORTA 9999
echo ============================================================================
echo.

:: Carregar configuração
call config.bat

:: Definir OCI CLI
if defined OCI_PATH (
    set "OCI_EXE=%OCI_PATH%\oci.exe"
) else (
    set "OCI_EXE=oci"
)

echo [1/5] Obtendo IP publico da VM...
for /f "tokens=*" %%i in ('%OCI_EXE% compute instance list-vnics --instance-id %INSTANCE_OCID% --query "data[0].\"public-ip\"" --raw-output --auth security_token') do set PUBLIC_IP=%%i

if "%PUBLIC_IP%"=="" (
    echo [ERRO] Nao foi possivel obter o IP publico
    pause
    exit /b 1
)

echo   IP Publico: %PUBLIC_IP%
echo.

echo [2/5] Copiando script de diagnostico para a VM...
scp -o StrictHostKeyChecking=no -i "%SSH_KEY_PATH%" "diagnose_port_9999.sh" %SSH_USER%@%PUBLIC_IP%:/tmp/
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao copiar script
    pause
    exit /b 1
)
echo   Script copiado com sucesso
echo.

echo [3/5] Executando diagnostico na VM...
echo ============================================================================
echo.
ssh -o StrictHostKeyChecking=no -i "%SSH_KEY_PATH%" %SSH_USER%@%PUBLIC_IP% "chmod +x /tmp/diagnose_port_9999.sh; /tmp/diagnose_port_9999.sh"
echo.

echo ============================================================================
echo [4/5] Testando conectividade externa (do seu computador)...
echo.
curl -v --max-time 5 http://%PUBLIC_IP%:9999/actuator/health
echo.

echo ============================================================================
echo [5/5] URLs para teste manual:
echo ============================================================================
echo.
echo   Health Check: http://%PUBLIC_IP%:9999/actuator/health
echo   GraphQL:      http://%PUBLIC_IP%:9999/graphql
echo   Login:        http://%PUBLIC_IP%:9999/login
echo   Frontend:     http://%PUBLIC_IP%
echo.
echo ============================================================================
echo   TESTE COMPLETO
echo ============================================================================
pause
