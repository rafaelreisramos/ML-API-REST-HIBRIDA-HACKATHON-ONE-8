# 🚑 Guia de Correção Manual: Modelo de IA

Este guia descreve como corrigir o erro *"Modelo offline"* ou *"FALHA FATAL: Sem modelo"* no serviço de IA (`ai_service`).

## O Problema

O arquivo binário do modelo de Machine Learning (`modelo_churn.joblib`) é muito grande e foi ignorado pelo git, resultando em um arquivo ausente ou corrompido (placeholder de texto) no seu clone local.

## A Solução

Você precisa obter o arquivo original com o time de Data Science e colocá-lo manualmente na pasta correta.

### Passo 1: Obter o Arquivo

Solicite ao time de DS o arquivo:

- **Nome:** `modelo_churn.joblib` (ou `modelo_churn_final_calibrado.joblib`, renomeie se necessário)
- **Tamanho Esperado:** Aprox. 50MB - 500MB (não pode ser 1KB!)

### Passo 2: Instalar

Copie o arquivo para a seguinte pasta no seu projeto:

`d:\2026 - HACKATHON ALURA\ML-API-REST-HIBRIDA-HACKATHON-ONE-8\ai_service\models\`

**Caminho final deve ser:**
`...\ai_service\models\modelo_churn.joblib`

> **Nota:** Se já existir um arquivo com esse nome (com tamanho pequeno/bytes), pode sobrescrevê-lo.

### Passo 3: Reiniciar Serviço

No terminal, reinicie o container da IA:

```powershell
docker-compose restart ai-service
```

### Passo 4: Verificar

Aguarde 10 segundos e verifique os logs:

```powershell
docker logs ai-service
```

Você deve ver:
`✅ [AI SERVICE] Modelo G8 carregado com SUCESSO.`
