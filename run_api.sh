#!/bin/bash

# Obtém o diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==========================================="
echo "  Iniciando API Spring Boot + GraphQL"
echo "==========================================="

MAVEN_VERSION="3.9.6"
MAVEN_DIR="apache-maven-${MAVEN_VERSION}"
MAVEN_TAR="${MAVEN_DIR}-bin.tar.gz"

if [ -f "${MAVEN_DIR}/bin/mvn" ]; then
    echo "[OK] Maven encontrado em ${MAVEN_DIR}"
else
    echo "[!] Maven não encontrado. Baixando versão portátil..."
    wget "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/${MAVEN_VERSION}/apache-maven-${MAVEN_VERSION}-bin.tar.gz" -O "${MAVEN_TAR}"
    
    echo "[!] Extraindo Maven..."
    tar -xzf "${MAVEN_TAR}"
    
    echo "[OK] Instalação concluída."
fi

echo ""
echo "-------------------------------------------"
echo "  Compilando e Rodando a Aplicação..."
echo "-------------------------------------------"
echo ""

"${MAVEN_DIR}/bin/mvn" spring-boot:run

read -p "Pressione Enter para continuar..."
