@echo off
setlocal
cd /d %~dp0

echo ===========================================
echo   Iniciando API Spring Boot + GraphQL
echo ===========================================

set MAVEN_VERSION=3.9.6
set MAVEN_DIR=apache-maven-%MAVEN_VERSION%
set MAVEN_ZIP=%MAVEN_DIR%-bin.zip

IF EXIST "%MAVEN_DIR%\bin\mvn.cmd" (
    echo [OK] Maven encontrado em %MAVEN_DIR%
    goto run
)

echo [!] Maven nao encontrado. Baixando versao portatil...
powershell -Command "Invoke-WebRequest -Uri https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/%MAVEN_VERSION%/apache-maven-%MAVEN_VERSION%-bin.zip -OutFile %MAVEN_ZIP%"

echo [!] Extraindo Maven...
powershell -Command "Expand-Archive -Path %MAVEN_ZIP% -DestinationPath . -Force"

echo [OK] Instalacao concluida.

:run
echo.
echo -------------------------------------------
echo   Compilando e Rodando a Aplicacao...
echo -------------------------------------------
echo.

"%MAVEN_DIR%\bin\mvn.cmd" spring-boot:run

pause
