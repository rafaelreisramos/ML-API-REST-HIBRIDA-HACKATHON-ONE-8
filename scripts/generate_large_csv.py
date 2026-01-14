import csv
import random
import uuid

# Configuração
FILENAME = "teste_50k_correto.csv"
NUM_RECORDS = 50000

# Colunas esperadas pelo sistema (CamelCase)
HEADERS = [
    "clienteId", "idade", "genero", "regiao", "valorMensal", 
    "tempoAssinaturaMeses", "planoAssinatura", "metodoPagamento", 
    "dispositivoPrincipal", "visualizacoesMes", "contatosSuporte", 
    "avaliacaoPlataforma", "avaliacaoConteudoMedia", 
    "avaliacaoConteudoUltimoMes", "tempoMedioSessaoMin", 
    "diasUltimoAcesso", "tipoContrato", "categoriaFavorita", "acessibilidade"
]

# Dados para aleatoriedade
REGIOES = ["Norte", "Sul", "Leste", "Oeste", "Sudeste", "Nordeste", "Centro-Oeste"]
GENEROS = ["Masculino", "Feminino", "Outro"]
PLANOS = ["basico", "padrao", "premium"]
METODOS = ["cartao_credito", "boleto", "pix", "debito"]
DISPOSITIVOS = ["mobile", "tablet", "desktop", "tv"]
CONTRATOS = ["MENSAL", "ANUAL", "SEMESTRAL"]
CATEGORIAS = ["FILMES", "SERIES", "DOCUMENTARIOS", "ESPORTES"]

def generate_row(index):
    return {
        "clienteId": f"BATCH-50K-{index:05d}",
        "idade": random.randint(18, 80),
        "genero": random.choice(GENEROS),
        "regiao": random.choice(REGIOES),
        "valorMensal": round(random.uniform(19.90, 89.90), 2),
        "tempoAssinaturaMeses": random.randint(1, 60),
        "planoAssinatura": random.choice(PLANOS),
        "metodoPagamento": random.choice(METODOS),
        "dispositivoPrincipal": random.choice(DISPOSITIVOS),
        "visualizacoesMes": random.randint(0, 100),
        "contatosSuporte": random.randint(0, 10),
        "avaliacaoPlataforma": round(random.uniform(1.0, 5.0), 1),
        "avaliacaoConteudoMedia": round(random.uniform(1.0, 5.0), 1),
        "avaliacaoConteudoUltimoMes": round(random.uniform(1.0, 5.0), 1),
        "tempoMedioSessaoMin": random.randint(10, 180),
        "diasUltimoAcesso": random.randint(0, 30),
        "tipoContrato": random.choice(CONTRATOS),
        "categoriaFavorita": random.choice(CATEGORIAS),
        "acessibilidade": random.choice([0, 1])
    }

print(f"🚀 Iniciando geração de {NUM_RECORDS} registros...")

with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=HEADERS)
    writer.writeheader()
    
    for i in range(1, NUM_RECORDS + 1):
        writer.writerow(generate_row(i))
        if i % 10000 == 0:
            print(f"   ... {i} linhas geradas")

print(f"✅ Arquivo '{FILENAME}' criado com sucesso!")
