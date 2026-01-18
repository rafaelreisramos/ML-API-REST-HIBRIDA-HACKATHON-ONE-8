import csv
import random
import uuid

# Configurações
FILENAME = "clientes_teste_100_variados.csv"
NUM_RECORDS = 100

# Definição das colunas (baseada no App.tsx e modelo esperado)
COLUNAS = [
    "clienteId", "idade", "genero", "regiao", "planoAssinatura", 
    "valorMensal", "tipoContrato", "tempoMedioSessaoMin", 
    "diasUltimoAcesso", "avaliacaoConteudoUltimoMes", "visualizacoesMes"
]

def gerar_registro(perfil):
    """Gera um registro baseado em um perfil de risco (alto/urgente/baixo)"""
    cliente_id = str(uuid.uuid4())[:8]
    genero = random.choice(["Masculino", "Feminino"])
    regiao = random.choice(["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"])
    
    if perfil == "URGENTE": # Churn Quase Certo (Cliente insatisfeito e inativo)
        idade = random.randint(18, 70)
        plano = random.choice(["basico", "padrao"])
        valor = random.choice([29.90, 49.90])
        contrato = "MENSAL" # Mais instável
        
        # Fatores Críticos
        tempo_sessao = random.randint(0, 10) # Sessões muito curtas
        dias_inativo = random.randint(15, 60) # Muito tempo sem acessar
        aval = 1 # Detrator
        views_mes = random.randint(0, 5) # Quase não assiste
        
    elif perfil == "ALTO": # Risco Alto (Cliente esfriando)
        idade = random.randint(18, 70)
        plano = random.choice(["basico", "padrao", "premium"])
        valor = random.choice([29.90, 49.90, 79.90])
        contrato = random.choice(["MENSAL", "ANUAL"])
        
        # Fatores Críticos
        tempo_sessao = random.randint(10, 30)
        dias_inativo = random.randint(7, 20)
        aval = random.randint(2, 3) # Neutro/Insatisfeito
        views_mes = random.randint(5, 15)
        
    else: # BAIXO (Cliente engajado)
        idade = random.randint(18, 70)
        plano = random.choice(["padrao", "premium"])
        valor = random.choice([49.90, 79.90])
        contrato = "ANUAL" # Mais fiel
        
        # Fatores Críticos
        tempo_sessao = random.randint(45, 120) # Viciado
        dias_inativo = random.randint(0, 3) # Acessa sempre
        aval = random.randint(4, 5) # Promotor
        views_mes = random.randint(20, 100)
    
    return [
        cliente_id, idade, genero, regiao, plano, valor, contrato,
        tempo_sessao, dias_inativo, aval, views_mes
    ]

# Geração dos dados
dados = []

# Distribuição: 30% Urgente, 30% Alto, 40% Baixo
for _ in range(30):
    dados.append(gerar_registro("URGENTE"))
    
for _ in range(30):
    dados.append(gerar_registro("ALTO"))
    
for _ in range(40):
    dados.append(gerar_registro("BAIXO"))

# Embaralhar para não ficar sequencial no arquivo
random.shuffle(dados)

# Escrever CSV
with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(COLUNAS)
    writer.writerows(dados)

print(f"Arquivo '{FILENAME}' gerado com sucesso com {NUM_RECORDS} registros.")
print("Distribuição aproximada: 30 Urgentes, 30 Alto Risco, 40 Baixo Risco.")
