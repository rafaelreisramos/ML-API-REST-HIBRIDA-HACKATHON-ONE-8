import pandas as pd
import os

input_file = "teste_dashboard_balanceado1.csv"
output_file = "teste_dashboard_balanceado1_fixed.csv"

if not os.path.exists(input_file):
    print(f"File {input_file} not found.")
    exit(1)

print(f"Reading {input_file}...")
df = pd.read_csv(input_file)

# Columns to fix (convert float to int)
# Based on log: visualizacoesMes is failing as 1.0
cols_to_fix = ['visualizacoesMes', 'chamadosSuporte', 'diasUltimoAcesso', 'idade', 'tempoAssinaturaMeses', 'dispositivosConectados', 'acessibilidade', 'tempoMedioSessaoMin', 'avaliacaoConteudoUltimoMes']

for col in cols_to_fix:
    if col in df.columns:
        print(f"Fixing column {col}...")
        # Fill NaNs with 0 or appropriate default if needed, though assumed full here
        df[col] = df[col].fillna(0).astype(int)

print(f"Saving to {output_file}...")
df.to_csv(output_file, index=False)
print("Done.")
