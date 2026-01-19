
import pandas as pd
import uuid

# Load original data
input_file = r"docs/csv/clientes_teste_100_variados.csv"
df = pd.read_csv(input_file)

# Target: 3500 records (approx < 5 mins with visualization delay)
target_count = 3500
repeats = (target_count // len(df)) + 1

# Duplicate
df_expanded = pd.concat([df] * repeats, ignore_index=True)
df_expanded = df_expanded.iloc[:target_count]

# Make IDs unique
df_expanded['clienteId'] = [str(uuid.uuid4())[:8] for _ in range(len(df_expanded))]

# Output
output_file = r"docs/csv/clientes_teste_stress_5min.csv"
df_expanded.to_csv(output_file, index=False)

print(f"Generated {len(df_expanded)} records in {output_file}")
