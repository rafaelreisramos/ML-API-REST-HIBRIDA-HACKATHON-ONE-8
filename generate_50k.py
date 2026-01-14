import csv
import random

FILE_50K = "teste_50k_correto.csv"

def generate_csv_50k():
    print(f"🔨 Gerando CSV com 50.000 registros em {FILE_50K}...")
    header = ["cliente_id", "idade", "genero", "tempo_assinatura_meses", "plano_assinatura", "valor_mensal", "visualizacoes_mes", "tempo_medio_sessao_min", "contatos_suporte", "avaliacao_conteudo_media", "avaliacao_conteudo_ultimo_mes", "avaliacao_plataforma", "regiao"]
    
    with open(FILE_50K, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        planos = ["Basico", "Premium", "Familia"]
        regioes = ["Norte", "Sul", "Leste", "Oeste", "Sudeste"]
        
        for i in range(50000):
            writer.writerow([
                f"CLI-{i:05d}",
                random.randint(18, 80),
                random.choice(["Masculino", "Feminino"]),
                random.randint(1, 60),
                random.choice(planos),
                round(random.uniform(20.0, 100.0), 2),
                random.randint(0, 50),
                random.randint(5, 120),
                random.randint(0, 10),
                round(random.uniform(1.0, 5.0), 1),
                round(random.uniform(1.0, 5.0), 1),
                round(random.uniform(1.0, 5.0), 1),
                random.choice(regioes)
            ])
    print(f"✅ CSV gerado com sucesso: {FILE_50K}")

if __name__ == "__main__":
    generate_csv_50k()
