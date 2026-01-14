import csv
import random

# Configuração
FILENAME = 'teste_1k_31churn.csv'
TOTAL_RECORDS = 1000
TARGET_CHURN_RATE = 0.31  # 31%

# Perfis
REGIOES = ['Norte', 'Sul', 'Sudeste', 'Nordeste', 'Centro-Oeste']
PLANOS = ['basico', 'padrao', 'premium']
GENEROS = ['Masculino', 'Feminino']
CONTRATOS = ['MENSAL', 'ANUAL', 'TRIMESTRAL']
CATEGORIAS = ['FILMES', 'ESPORTES', 'SERIES', 'DOCUMENTARIOS']

def generate_high_risk(id_num):
    """Gera um cliente com características de ALTO churn"""
    return {
        'clienteId': f'TEST-31PC-{id_num:04d}',
        'idade': random.randint(18, 70),
        'genero': random.choice(GENEROS),
        'regiao': random.choice(REGIOES),
        'valorMensal': round(random.uniform(29.90, 150.00), 2),
        # CARACTERÍSTICAS DE RISCO:
        'tempoAssinaturaMeses': random.randint(1, 3), # Cliente novo
        'planoAssinatura': 'premium' if random.random() > 0.3 else random.choice(PLANOS), # Premium tende a exigir mais
        'visualizacoesMes': random.randint(0, 5), # Não usa a plataforma
        'contatosSuporte': random.randint(5, 20), # Reclama muito
        'avaliacaoPlataforma': round(random.uniform(1.0, 2.5), 1), # Odeia a plataforma
        'tipoContrato': 'MENSAL', # Fácil de cancelar
        'categoriaFavorita': random.choice(CATEGORIAS)
    }

def generate_low_risk(id_num):
    """Gera um cliente FIEL"""
    return {
        'clienteId': f'TEST-31PC-{id_num:04d}',
        'idade': random.randint(18, 70),
        'genero': random.choice(GENEROS),
        'regiao': random.choice(REGIOES),
        'valorMensal': round(random.uniform(29.90, 89.90), 2),
        # CARACTERÍSTICAS DE RETENÇÃO:
        'tempoAssinaturaMeses': random.randint(12, 60), # Cliente antigo
        'planoAssinatura': 'basico' if random.random() > 0.5 else 'padrao',
        'visualizacoesMes': random.randint(20, 100), # Heavy user
        'contatosSuporte': random.randint(0, 1), # Nunca reclama
        'avaliacaoPlataforma': round(random.uniform(4.0, 5.0), 1), # Ama
        'tipoContrato': 'ANUAL' if random.random() > 0.4 else 'MENSAL',
        'categoriaFavorita': random.choice(CATEGORIAS)
    }

data = []
num_high_risk = int(TOTAL_RECORDS * TARGET_CHURN_RATE)
num_low_risk = TOTAL_RECORDS - num_high_risk

print(f"Gerando dataset com {TOTAL_RECORDS} registros...")
print(f"Alvo: {num_high_risk} Alto Risco (31%) | {num_low_risk} Baixo Risco")

# Gerar dados
for i in range(num_high_risk):
    data.append(generate_high_risk(i))

for i in range(num_high_risk, TOTAL_RECORDS):
    data.append(generate_low_risk(i))

# Embaralhar para não ficar sequencial
random.shuffle(data)

# Salvar CSV
headers = list(data[0].keys())
with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Arquivo '{FILENAME}' gerado com sucesso!")
