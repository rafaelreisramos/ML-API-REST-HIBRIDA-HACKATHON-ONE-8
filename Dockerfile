# --- Estágio 1: Build (Compilação) ---
# Usamos uma imagem com Maven pré-instalado para gerar o .jar
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copiar arquivos de projeto
COPY pom.xml .
COPY src ./src

# Compilar (Pulando testes para ser mais rápido agora)
RUN mvn clean package -DskipTests

# --- Estágio 2: Runtime (Execução) ---
# Usamos uma imagem leve apenas com o Java (JRE) para rodar
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Token padrão para garantir inicialização sem falhas
ENV JWT_TOKEN="hackathon_build_token_default"

# Copiar o JAR gerado no estágio anterior
COPY --from=build /app/target/*.jar app.jar

# Expor a porta que definimos (9999)
EXPOSE 9999

# Comando para rodar
ENTRYPOINT ["java", "-jar", "app.jar"]
