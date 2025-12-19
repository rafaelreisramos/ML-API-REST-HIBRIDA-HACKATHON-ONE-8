
import csv
import random

input_path = r'd:\HACKATHON_API\spring_graphql_mongo\test_1300_fixed.csv'
output_path = r'd:\HACKATHON_API\spring_graphql_mongo\test_churn_30pct.csv'

print(f"Reading {input_path}...")

rows = []
header = ""

with open(input_path, 'r', encoding='utf-8') as f_in:
    lines = f_in.readlines()
    header = lines[0].strip()
    for line in lines[1:]:
        rows.append(line.strip().split(','))

# Target: 30% of total
total = len(rows)
target_churn = int(total * 0.3)

print(f"Total: {total}. Target Churners: {target_churn}")

# Randomly select indices to become "Churners"
churn_indices = random.sample(range(total), target_churn)

# Headers mapping (based on previous fix script)
# 0:clienteId, 1:idade, 2:genero, 3:regiao, 4:valorMensal, 5:tempoAssinaturaMeses, 
# 6:planoAssinatura, 7:metodoPagamento, 8:dispositivoPrincipal, 9:visualizacoesMes, 
# 10:contatosSuporte, 11:avaliacaoPlataforma, 12:avaliacaoConteudoMedia, 
# 13:avaliacaoConteudoUltimoMes, 14:tempoMedioSessaoMin, 15:diasUltimoAcesso

for idx in churn_indices:
    row = rows[idx]
    
    # Modify features to induce Churn (Hypothesis based on common churn drivers)
    
    # 1. Low visualizacoesMes (idx 9) -> 0 to 5
    row[9] = str(random.randint(0, 5))
    
    # 2. High diasUltimoAcesso (idx 15) -> 30 to 90
    row[15] = str(random.randint(30, 90))
    
    # 3. Low avaliacaoPlataforma (idx 11) -> 1.0 to 2.5
    row[11] = f"{random.uniform(1.0, 2.5):.1f}"
    
    # 4. Low avaliacaoConteudoUltimoMes (idx 13) -> 1.0 to 2.0
    row[13] = f"{random.uniform(1.0, 2.0):.1f}"
    
    # 5. Short tempoAssinaturaMeses (idx 5) -> New user frustration? or just standard.
    # Let's keep signature time random or low.
    # row[5] = str(random.randint(1, 3)) 

    # 6. High contatosSuporte (idx 10) -> Clamor for help
    row[10] = str(random.randint(3, 8))

print(f"Modified {len(churn_indices)} rows to simulate churn characteristics.")

with open(output_path, 'w', encoding='utf-8') as f_out:
    f_out.write(header + "\n")
    for row in rows:
        f_out.write(",".join(row) + "\n")

print("Done.")
