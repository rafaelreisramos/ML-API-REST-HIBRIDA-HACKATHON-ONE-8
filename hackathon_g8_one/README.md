# Documentação: Arquivo `.joblib` e Recursos do Modelo de Churn

## 📋 Sumário Executivo

Este documento descreve o **arquivo principal do modelo** (`modelo_churn.joblib`) e todos os **arquivos de suporte** necessários para que a **API REST (Java/Spring Boot)** consiga carregar o modelo e fazer previsões de churn em tempo real.

---

## 🎯 O que é o arquivo `.joblib`?

O arquivo **`modelo_churn.joblib`** é um arquivo **serializado em formato binário** que contém:

- ✅ Modelo de classificação treinado (Random Forest com calibração de probabilidade)
- ✅ Pesos e parâmetros aprendidos durante o treinamento
- ✅ Configurações otimizadas do modelo

**Importante:** Ele **NÃO contém** informações sobre pré-processamento, seleção de features ou mapeamento de variáveis categóricas. Por isso, os **arquivos de suporte são obrigatórios**.

---

## 📦 Arquivos Necessários e Sua Função

### **1. Modelo Serializado**

#### `modelo_churn.joblib`
- **O quê:** Modelo Random Forest com calibração de probabilidade
- **Tamanho:** 29 MB
- **Função:** Realizar predições de churn
- **Carregamento em Python:**
  ```python
  import joblib
  modelo = joblib.load('modelo_churn.joblib')
  ```
- **Uso na API:** Receber dados do cliente e retornar previsão + probabilidade

---

### **2. Seletor de Features (RFE)**

#### `rfe_selector.joblib`
- **O quê:** Objeto de Recursive Feature Elimination (RFE) que selecionou as melhores features
- **Função:** Filtrar apenas as features relevantes antes de passar para o modelo
- **Por quê é necessário:** O modelo foi treinado com um **subset específico de features**. Se a API enviar todas as features originais, o modelo falhará
- **Carregamento em Python:**
  ```python
  rfe = joblib.load('rfe_selector.joblib')
  X_selecionado = rfe.transform(X_novo)
  ```
- **Fluxo:** API recebe dados → RFE filtra → Modelo prediz

---

### **3. Threshold Ótimo**

#### `threshold_otimo.txt`
- **O quê:** Valor numérico do threshold de decisão otimizado
- **Formato:** Arquivo texto com um único valor (`0.4287`)
- **Função:** Converter probabilidade bruta em previsão binária ("Vai cancelar" / "Vai continuar")
- **Por quê:** O modelo retorna probabilidade (0.0 a 1.0). Este threshold define: se `prob > threshold` → "Vai cancelar", senão → "Vai continuar"
- **Leitura em Python:**
  ```python
  with open('threshold_otimo.txt', 'r') as f:
      threshold = float(f.read().strip())
  ```
- **Fluxo na API:**
  ```
  Probabilidade = 0.76
  Threshold = 0.4287
  Se 0.76 > 0.4287 → "Vai cancelar" ✓
  ```

---

### **4. Mapeamento de Codificadores Categóricos**

#### `label_encoders_info.txt`
- **O quê:** Informações sobre como variáveis categóricas foram codificadas (ex: "Feminino" → FEMININO)
- **Formato:** Arquivo texto com dicionário ou lista de mapeamentos
- **Exemplo de conteúdo:**
  ```
  tipo_contrato: {'ANUAL': 0, 'MENSAL': 1}
  plano_assinatura: {'BÁSICO': 0, 'PADRÃO': 1, 'PREMIUM': 2}
  ```
- **Função:** Converter entrada textual da API para número (formato que o modelo espera)
- **Leitura em Python:**
  ```python
  import json
  with open('label_encoders_info.txt', 'r') as f:
      encoders = json.load(f)
  ```

---

### **5. Features Selecionadas pelo RFE**

#### `features_selecionadas_rfe.csv`
- **O quê:** Lista das features que o modelo espera receber (após RFE)
- **Formato:** CSV com uma coluna "feature_name" ou lista simples
- **Exemplo:**
  ```
  idade
  genero
  regiao
  tipo_contrato
  metodo_pagamento
  ```
- **Função:** Validação na API (verificar se todas as features obrigatórias foram enviadas)
- **Leitura em Python:**
  ```python
  import pandas as pd
  features = pd.read_csv('features_selecionadas_rfe.csv')['idade'].tolist()
  ```

---

### **6. Melhores Hiperparâmetros**

#### `melhores_hiperparametros.csv`
- **O quê:** Parâmetros otimizados do Random Forest usados no treinamento
- **Formato:** CSV com colunas como "parametro" e "valor"
- **Exemplo:**
  ```
  parametro,valor
  n_estimators,100
  max_depth,None
  min_samples_split,5
  ```
- **Função:** Documentação (para reprodutibilidade e compreensão do modelo)
- **Nota:** O arquivo `.joblib` já contém esses parâmetros. Este arquivo é para **referência e auditoria**.

---

### **7. Dados de Treinamento e Teste**

#### `X_train.csv` | `y_train.csv` | `X_test.csv` | `y_test.csv`
- **O quê:** Conjunto completo de dados usado no treinamento e teste
- **Função:** 
  - 📊 **Documentação:** Mostrar aos avaliadores a origem dos dados
  - 🔍 **Validação:** Calcular métricas de desempenho (Acurácia, Precisão, Recall, F1)
  - 🧪 **Testes automatizados:** Usar para validar que a API retorna as mesmas previsões
  - 📈 **Estatísticas:** Explicar distribuição de features e classes
- **Nota:** Estes arquivos **não são necessários** para o funcionamento da API em produção, mas são **essenciais para demonstração e validação**.

---

## 🚀 Como Usar na API (Sugestão de Fluxo Prático)

### **Passo 1: Carregamento Único (na inicialização da API)**

```python
# app.py ou config.py
import joblib
import pandas as pd
import json

# Carregar modelo
modelo = joblib.load('modelo_churn.joblib')

# Carregar seletor RFE
rfe = joblib.load('rfe_selector.joblib')

# Carregar threshold
with open('threshold_otimo.txt', 'r') as f:
    threshold = float(f.read().strip())

# Carregar label encoders
with open('label_encoders_info.txt', 'r') as f:
    encoders = json.load(f)

# Carregar features esperadas
features_df = pd.read_csv('features_selecionadas_rfe.csv')
features_esperadas = features_df['idade'].tolist()
```

### **Passo 2: Endpoint de Predição**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    POST /predict
    Body JSON:
    {
        "tempo_assinatura_meses": 12,
        "plano_assinatura": "Premium",
        "dias_ultimo_acesso": 5
    }
    """
    
    # 1. Receber dados
    dados = request.json
    
    # 2. Codificar variáveis categóricas
    for chave, valor in dados.items():
        if chave in encoders:
            dados[chave] = encoders[chave].get(valor, -1)
    
    # 3. Criar DataFrame com mesma ordem de features
    X = pd.DataFrame([dados])[features_esperadas]
    
    # 4. Aplicar RFE (seleção de features)
    X_selecionado = rfe.transform(X)
    
    # 5. Predizer
    probabilidade = modelo.predict_proba(X_selecionado)[0][1]  # Classe "Vai cancelar"
    
    # 6. Aplicar threshold
    previsao = "Vai cancelar" if probabilidade > threshold else "Vai continuar"
    
    return jsonify({
        "previsao": previsao,
        "probabilidade": round(probabilidade, 4),
        "threshold_usado": threshold
    })
```

### **Passo 3: Exemplo de Requisição e Resposta**

**Requisição:**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tempo_assinatura_meses": 12,
    "plano_assinatura": "Premium",
    "dias_ultimo_acesso": 5
  }'
```

**Resposta:**
```json
{
  "previsao": "Vai cancelar",
  "probabilidade": 0.7634,
  "threshold_usado": 0.4287
}
```

---

## ✅ Checklist de Integração na API

- [ ] Arquivo `modelo_churn.joblib` carregado na inicialização
- [ ] Arquivo `rfe_selector.joblib` disponível e aplicado antes da predição
- [ ] Arquivo `threshold_otimo.txt` lido corretamente
- [ ] Arquivo `label_encoders_info.txt` usado para transformar variáveis categóricas
- [ ] Arquivo `features_selecionadas_rfe.csv` valida entrada (todas as features presentes)
- [ ] Ordem das features preservada (crítico!)
- [ ] Endpoint retorna `previsao` e `probabilidade` em JSON

---

## 📊 Informações para Documentação da Solução

### **Desempenho do Modelo (com X_test.csv e y_test.csv)**

Calcule e documente:

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

y_pred = modelo.predict(X_test_selecionado)
y_pred_proba = modelo.predict_proba(X_test_selecionado)[:, 1]

print(f"Acurácia: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precisão: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
```

### **Estatísticas dos Dados**

```python
# Com X_train.csv e y_train.csv
print(f"Total de registros: {len(X_train)}")
print(f"Taxa de churn: {y_train.mean():.2%}")
print(f"Features utilizadas: {len(features_esperadas)}")
print(f"Threshold otimizado: {threshold}")
```

---

## 🔗 Estrutura de Arquivos Recomendada

```
projeto-churn/
├── models/
│   ├── modelo_churn.joblib
│   ├── rfe_selector.joblib
│   ├── threshold_otimo.txt
│   ├── label_encoders_info.txt
│   └── features_selecionadas_rfe.csv
├── data/
│   ├── X_train.csv
│   ├── y_train.csv
│   ├── X_test.csv
│   ├── y_test.csv
│   └── melhores_hiperparametros.csv
├── api/
│   ├── app.py (ou main Java)
│   ├── requirements.txt
│   └── test_predict.py
└── README.md
```

---

## 🎓 Resumo: O que Anexar no Hackathon

### **Obrigatório para Funcionamento:**
1. ✅ `modelo_churn.joblib`
2. ✅ `rfe_selector.joblib`
3. ✅ `threshold_otimo.txt`
4. ✅ `label_encoders_info.txt`
5. ✅ `features_selecionadas_rfe.csv`

### **Recomendado para Validação:**
6. ✅ `melhores_hiperparametros.csv` (reprodutibilidade)
7. ✅ `X_test.csv` + `y_test.csv` (demonstrar desempenho)

### **Opcional (mas útil):**
8. ⚪ `X_train.csv` + `y_train.csv` (documentação completa)

---

## ⚠️ Erros Comuns a Evitar

| Erro | Causa | Solução |
|------|-------|--------|
| `ValueError: X has 50 features but model expects 20` | Ordem ou número de features incorreto | Aplicar RFE antes de predizer |
| `KeyError: 'plano_assinatura'` | Variável categórica não foi codificada | Usar `label_encoders_info.txt` |
| `Probabilidade sempre 0.5` | Threshold não foi carregado | Verificar `threshold_otimo.txt` |
| `FileNotFoundError` | Arquivos não estão no diretório certo | Usar caminhos absolutos ou variáveis de ambiente |

---

## 📞 Perguntas Frequentes

**P: Posso usar apenas o arquivo `.joblib` sem os outros?**
R: Não. O modelo depende de RFE, label encoders e threshold para funcionar corretamente.

**P: A ordem das features importa?**
R: Sim, **é crítica**. Features devem estar na mesma ordem usada no treinamento.

**P: Preciso dos arquivos CSV de dados?**
R: Para a API funcionar, não. Mas para demonstrar desempenho aos avaliadores, sim.

**P: Como testor a API localmente?**
R: Use o `X_test.csv` com `y_test.csv` para validar que as previsões estão corretas.

---

**Última atualização:** 10 de Janeiro de 2026.
**Status:** Pronto para produção ✅
