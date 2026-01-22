#!/bin/bash
# Script para teste de requisição via cURL

echo "=== Teste de Requisição cURL - ChurnInsight API ==="
echo ""

# 1. Verificar health
echo "1. Health Check:"
curl -s http://localhost:9999/actuator/health
echo ""
echo ""

# 2. Testar AI Service diretamente
echo "2. Teste AI Service (porta 5000):"
curl -s http://localhost:5000/docs | head -c 200
echo ""
echo ""

# 3. Fazer uma previsão direta no AI Service
echo "3. Previsão no AI Service:"
curl -s -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 35,
    "tempoAssinaturaMeses": 6,
    "planoAssinatura": "Padrao",
    "valorMensal": 59.90,
    "visualizacoesMes": 10,
    "contatosSuporte": 3,
    "metodoPagamento": "Credito",
    "dispositivoPrincipal": "Mobile",
    "avaliacaoConteudoMedia": 3.0,
    "avaliacaoConteudoUltimoMes": 2.5,
    "tempoMedioSessaoMin": 25,
    "diasUltimoAcesso": 15,
    "avaliacaoPlataforma": 3.5,
    "regiao": "Sudeste",
    "genero": "Masculino",
    "tipoContrato": "MENSAL",
    "categoriaFavorita": "SERIES",
    "acessibilidade": 0
  }'
echo ""
echo ""

# 4. Teste GraphQL
echo "4. Listar Análises via GraphQL:"
curl -s -X POST http://localhost:9999/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{listarAnalises{clienteId previsao probabilidade}}"}'
echo ""

echo ""
echo "=== Fim do Teste ==="
