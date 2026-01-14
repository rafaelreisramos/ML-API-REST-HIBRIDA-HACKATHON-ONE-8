import csv
import random

# Configuração
FILENAME = 'teste_extremo_1k.csv'
TOTAL_RECORDS = 1000
TARGET_HIGH_RISK = 0.45  # 45% devem ultrapassar threshold de 42.87%

# Perfis
REGIOES = ['Norte', 'Sul', 'Sudeste', 'Nordeste', 'Centro-Oeste', 'Leste', 'Oeste']
PLANOS = ['basico', 'padrao', 'premium']
GENEROS = ['Masculino', 'Feminino']
CONTRATOS = ['MENSAL', 'ANUAL', 'TRIMESTRAL']
CATEGORIAS = ['FILMES', 'ESPORTES', 'SERIES', 'DOCUMENTARIOS']

def generate_extreme_high_risk(id_num):
    """Gera um cliente com características EXTREMAS de churn (> 43% probabilidade esperada)"""
    return {
        'clienteId': f'EXTREME-{id_num:04d}',
        'idade': random.randint(18, 25),  # Jovens tendem a trocar mais
        'genero': random.choice(GENEROS),
        'regiao': random.choice(REGIOES),
        'valorMensal': round(random.uniform(120.00, 200.00), 2),  # Premium caro
        # CARACTERÍSTICAS EXTREMAS:
        'tempoAssinaturaMeses': 1,  # SEMPRE cliente novo (1 mês)
        'planoAssinatura': 'premium' if random.random() > 0.2 else 'padrao',  # 80% premium
        'visualizacoesMes': 0,  # NUNCA usa (0 visualizações)
        'contatosSuporte': random.randint(20, 30),  # MUITAS reclamações
        'avaliacaoPlataforma': round(random.uniform(1.0, 1.3), 1),  # ODEIA (nota 1.0-1.3)
        'tipoContrato': 'MENSAL',  # Fácil de cancelar
        'categoriaFavorita': random.choice(CATEGORIAS)
    }

def generate_moderate_risk(id_num):
    """Gera cliente com risco moderado (20-40% probabilidade)"""
    return {
        'clienteId': f'EXTREME-{id_num:04d}',
        'idade': random.randint(25, 50),
        'genero': random.choice(GENEROS),
        'regiao': random.choice(REGIOES),
        'valorMensal': round(random.uniform(50.00, 100.00), 2),
        'tempoAssinaturaMeses': random.randint(3, 8),  # Cliente médio
        'planoAssinatura': random.choice(['basico', 'padrao']),
        'visualizacoesMes': random.randint(5, 15),  # Uso moderado
        'contatosSuporte': random.randint(3, 8),  # Algumas reclamações
        'avaliacaoPlataforma': round(random.uniform(2.5, 3.5), 1),  # Neutro
        'tipoContrato': random.choice(['MENSAL', 'TRIMESTRAL']),
        'categoriaFavorita': random.choice(CATEGORIAS)
    }

def generate_low_risk(id_num):
    """Gera cliente fiel (< 20% probabilidade)"""
    return {
        'clienteId': f'EXTREME-{id_num:04d}',
        'idade': random.randint(30, 65),
        'genero': random.choice(GENEROS),
        'regiao': random.choice(REGIOES),
        'valorMensal': round(random.uniform(29.90, 79.90), 2),
        'tempoAssinaturaMeses': random.randint(18, 60),  # Cliente antigo
        'planoAssinatura': 'basico' if random.random() > 0.3 else 'padrao',
        'visualizacoesMes': random.randint(30, 120),  # Heavy user
        'contatosSuporte': random.randint(0, 1),  # Quase nunca reclama
        'avaliacaoPlataforma': round(random.uniform(4.5, 5.0), 1),  # Ama
        'tipoContrato': 'ANUAL' if random.random() > 0.3 else 'TRIMESTRAL',
        'categoriaFavorita': random.choice(CATEGORIAS)
    }

# Distribuição estratégica
num_extreme = int(TOTAL_RECORDS * TARGET_HIGH_RISK)  # 450
num_moderate = int(TOTAL_RECORDS * 0.30)  # 300
num_low = TOTAL_RECORDS - num_extreme - num_moderate  # 250

print(f"🎯 Gerando dataset EXTREMO com {TOTAL_RECORDS} registros...")
print(f"   📍 {num_extreme} Alto Risco (>43% esperado)")
print(f"   📍 {num_moderate} Risco Médio (20-40%)")
print(f"   📍 {num_low} Baixo Risco (<20%)")

data = []

# Gerar dados
for i in range(num_extreme):
    data.append(generate_extreme_high_risk(i))

for i in range(num_extreme, num_extreme + num_moderate):
    data.append(generate_moderate_risk(i))

for i in range(num_extreme + num_moderate, TOTAL_RECORDS):
    data.append(generate_low_risk(i))

# Embaralhar
random.shuffle(data)

# Salvar CSV
headers = list(data[0].keys())
with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Arquivo '{FILENAME}' gerado com sucesso!")
print(f"📊 Use este arquivo para testar o threshold de 42.87% do modelo.")
