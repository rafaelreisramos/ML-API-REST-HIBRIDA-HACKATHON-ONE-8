@echo off
:: ==================================================================================
::  VIBECODE ENGINEERING TOOL - OCI EDITION (V 1.0.0)
:: ==================================================================================
::  Artifact:    CONTROLE_OCI.bat
::  Module:      Cloud Infrastructure Automation (Oracle Cloud)
::  Author:      Araken Carmo Neto (Migrated by Antigravity)
::  Copyright:   (c) 2026 VibeCode Systems. All rights reserved.
::  Description: Enterprise-grade orchestration script for OCI Compute instances.
:: ==================================================================================

setlocal EnableDelayedExpansion

:: --- [ LOAD CONFIGURATION ] ---
if not exist config.bat (
    color 0C
    echo [ERROR] Configuration file 'config.bat' not found!
    echo.
    echo Please copy 'config.bat.example' to 'config.bat' and edit it with your OCI details.
    echo.
    pause
    exit /b 1
)
call config.bat

:: --- [ CONFIGURATION VALIDATION ] ---
if "%INSTANCE_OCID%"=="" (
    color 0E
    echo [WARNING] INSTANCE_OCID is not configured in 'config.bat'.
    pause
    exit /b 1
)

:: --- [ INITIALIZATION ] ---
:: Define OCI Executable
if defined OCI_PATH (
    set "OCI_EXE=%OCI_PATH%\oci.exe"
) else (
    set "OCI_EXE=oci"
)
set "OCI_FLAGS=--auth security_token"

color 0B
title VIBECODE OCI CONTROLLER [Initializing...]

:: --- [ DEPENDENCY CHECK ] ---
call :LOG "System initialization started."
call :LOG "Checking OCI CLI binary presence..."

if defined OCI_PATH (
    if not exist "!OCI_EXE!" (
         echo [CRITICAL ERROR] OCI CLI not found at !OCI_EXE!
         pause
         exit /b 1
    )
) else (
    where oci >nul 2>nul
    if !errorlevel! neq 0 (
        echo [CRITICAL ERROR] OCI CLI not found in PATH.
        pause
        exit /b 1
    )
)
call :LOG "Dependency check passed. OCI CLI is available."

:MAIN_MENU
cls
echo.
echo  _____   ______   _____   __  __   ____    _____   _       ___   __
echo ^|  __ \ ^|  ____^| / ____^| ^|  \/  ^| ^|  _ \  / ____^| ^| ^|     ^| \ \ / /
echo ^| ^|__) ^|^| ^|__   ^| (___   ^| \  / ^| ^| ^|_) ^|^| ^|      ^| ^|     ^| ^|\ V / 
echo ^|  _  / ^|  __^|   \___ \  ^| ^|\/^| ^| ^|  _ ^< ^| ^|      ^| ^|     ^| ^| ^> ^<  
echo ^| ^| \ \ ^| ^|____  ____) ^| ^| ^|  ^| ^| ^| ^|_) ^|^| ^|____  ^| ^|____ ^| ^|/ . \ 
echo ^|_^|  \_\^|______^|^|_____/  ^|_^|  ^|_^| ^|____/  \_____^| ^|______^|^|_^/_/ \_\ OCI EDITION
echo.
echo                  [  ORACLE CLOUD INFRASTRUCTURE MANAGER  ]
echo            Migrated for: ChurnInsight Infrastructure
echo ===================================================================
echo   Instance : ...%INSTANCE_OCID:~-12%
echo   User     : %SSH_USER%
echo   Rate     : $%COST_PER_HOUR%/hr (Estimated)
echo ===================================================================
echo.
echo   [1] START Instance      (Instance Action: START)
echo   [2] STOP Instance       (Instance Action: SOFTSTOP)
echo   [3] HEALTH CHECK        (Get Status ^& Public IP)
echo   [4] SECURE SHELL        (Auto SSH w/ IP Discovery)
echo   [5] VIEW LOGS           (Audit Trail)
echo   [0] EXIT
echo.
echo ===================================================================
set "op="
set /p op="SELECT ACTION > "

if not defined op (
    echo.
    echo [!] Nenhuma opcao selecionada. Encerrando programa...
    ping -n 3 127.0.0.1 >nul
    exit /b
)

if "%op%"=="1" goto START_VM
if "%op%"=="2" goto STOP_VM
if "%op%"=="3" goto STATUS_VM
if "%op%"=="4" goto SSH_VM
if "%op%"=="5" goto VIEW_LOGS
if "%op%"=="0" exit

echo.
echo [!] Opcao desconhecida: %op%
ping -n 3 127.0.0.1 >nul
goto MAIN_MENU

:START_VM
cls
echo [VIBECODE] Initiating OCI Boot Sequence...
call :LOG "User requested VM START."

:: Check status
echo [*] Checking current state...
for /f "tokens=*" %%i in ('!OCI_EXE! compute instance get --instance-id %INSTANCE_OCID% --query "data.\"lifecycle-state\"" --raw-output %OCI_FLAGS%') do set STATUS=%%i

if "%STATUS%"=="RUNNING" (
    echo [INFO] Instance is already RUNNING.
    call :LOG "Action skipped: VM already running."
    pause
    goto MAIN_MENU
)

echo [*] Sending START signal to OCI Control Plane...
call !OCI_EXE! compute instance action --instance-id %INSTANCE_OCID% --action START %OCI_FLAGS% >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Start signal sent. Instance is provisioning.
    call :LOG "VM Start command executed successfully."
) else (
    color 0C
    echo [ERROR] Failed to start instance. Check connectivity or permissions.
    call :LOG "ERROR: VM Start command failed."
)
echo.
pause
goto MAIN_MENU

:STOP_VM
cls
echo [VIBECODE] Initiating OCI Shutdown Sequence...
call :LOG "User requested VM STOP."

echo [*] Requesting SOFTSTOP...
call !OCI_EXE! compute instance action --instance-id %INSTANCE_OCID% --action SOFTSTOP %OCI_FLAGS% >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Stop signal sent. Instance is stopping.
    call :LOG "VM Stop command executed successfully."
) else (
    echo [ERROR] Failed to stop instance.
    call :LOG "ERROR: VM Stop command failed."
)
echo.
pause
goto MAIN_MENU

:STATUS_VM
cls
echo [VIBECODE] Retrieving OCI Telemetry...
call :LOG "User requested STATUS check."
echo.

:: Get Status
for /f "tokens=*" %%i in ('!OCI_EXE! compute instance get --instance-id %INSTANCE_OCID% --query "data.\"lifecycle-state\"" --raw-output %OCI_FLAGS%') do set STATUS=%%i
echo   Status     : %STATUS%
call :LOG "VM Status: %STATUS%"

:: Get Shape
for /f "tokens=*" %%i in ('!OCI_EXE! compute instance get --instance-id %INSTANCE_OCID% --query "data.shape" --raw-output %OCI_FLAGS%') do set SHAPE=%%i
echo   Shape      : %SHAPE%

if "%STATUS%"=="RUNNING" (
    echo.
    echo   [*] Fetching Public IP...
    :: Complex logic to find Public IP via VNIC attachments
    for /f "tokens=*" %%i in ('!OCI_EXE! compute instance list-vnics --instance-id %INSTANCE_OCID% --query "data[0].\"public-ip\"" --raw-output %OCI_FLAGS%') do set PUBLIC_IP=%%i
    echo   Public IP  : !PUBLIC_IP!
)

echo.
echo ========================================================
echo.
pause
goto MAIN_MENU

:SSH_VM
cls
echo [VIBECODE] Establishing Secure Tunnel...
call :LOG "User requested SSH connection."

:: 1. Check if Running
echo [*] Verifying instance state...
for /f "tokens=*" %%i in ('!OCI_EXE! compute instance get --instance-id %INSTANCE_OCID% --query "data.\"lifecycle-state\"" --raw-output %OCI_FLAGS%') do set STATUS=%%i

if "%STATUS%" NEQ "RUNNING" (
    color 0E
    echo [WARNING] Instance is NOT RUNNING (Current: %STATUS%).
    echo Cannot establish SSH connection. Please Start the VM first.
    call :LOG "SSH aborted: VM not running."
    pause
    color 0B
    goto MAIN_MENU
)

:: 2. Get Public IP dynamically
echo [*] resolving Public IP Address...
for /f "tokens=*" %%i in ('!OCI_EXE! compute instance list-vnics --instance-id %INSTANCE_OCID% --query "data[0].\"public-ip\"" --raw-output %OCI_FLAGS%') do set PUBLIC_IP=%%i

if "%PUBLIC_IP%"=="" (
    echo [ERROR] Could not resolve Public IP. Check if instance has a public IP assigned.
    pause
    goto MAIN_MENU
)

echo [*] IP Resolved: %PUBLIC_IP%
echo [*] Connecting as %SSH_USER%...

:: 3. Connect via SSH
echo.
ssh -o StrictHostKeyChecking=no -i "%SSH_KEY_PATH%" %SSH_USER%@%PUBLIC_IP%

if %errorlevel% equ 0 (
    call :LOG "SSH session ended normally."
) else (
    call :LOG "SSH session ended with errors."
)
echo.
pause
goto MAIN_MENU

:VIEW_LOGS
cls
echo [VIBECODE] Audit Log (%LOG_FILE%)
echo ========================================================
more %LOG_FILE%
echo ========================================================
echo.
pause
goto MAIN_MENU

:: --- [ HELPER FUNCTIONS ] ---
:LOG
set "MSG=%~1"
set "TIMESTAMP=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2% %TIME:~0,8%"
echo [%TIMESTAMP%] %MSG% >> %LOG_FILE%
exit /b
