import pandas as pd
import numpy as np
import random

# Seed para reprodutibilidade
np.random.seed(32)
random.seed(32)

n_registros = 50

data = {
    'clienteId': [f'TEST-BATCH-{i:03d}' for i in range(n_registros)],
    'idade': np.random.randint(18, 90, n_registros),
    'genero': np.random.choice(['Masculino', 'Feminino', 'Outro'], n_registros),
    'regiao': np.random.choice(['Sudeste', 'Sul', 'Norte', 'Nordeste', 'Centro-Oeste'], n_registros),
    'tempoAssinaturaMeses': np.random.randint(1, 60, n_registros),
    'planoAssinatura': np.random.choice(['basico', 'padrao', 'premium'], n_registros),
    'valorMensal': np.round(np.random.uniform(19.90, 99.90, n_registros), 2),
    'visualizacoesMes': np.random.randint(0, 100, n_registros),
    'tempoMedioSessaoMin': np.random.randint(10, 180, n_registros),
    'contatosSuporte': np.random.choice([0, 1, 2, 3, 5, 10], n_registros, p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05]),
    'avaliacaoConteudoMedia': np.round(np.random.uniform(1, 5, n_registros), 1),
    'avaliacaoConteudoUltimoMes': np.round(np.random.uniform(1, 5, n_registros), 1),
    'avaliacaoPlataforma': np.round(np.random.uniform(1, 5, n_registros), 1),
    'diasUltimoAcesso': np.random.randint(0, 30, n_registros),
    'metodoPagamento': np.random.choice(['credito', 'boleto', 'pix'], n_registros),
    'dispositivoPrincipal': np.random.choice(['mobile', 'desktop', 'tv'], n_registros),
    
    # Novos Campos V8
    'tipoContrato': np.random.choice(['MENSAL', 'ANUAL'], n_registros),
    'categoriaFavorita': np.random.choice(['FILMES', 'SERIES', 'DOCUMENTARIOS', 'ESPORTES', 'NOVELAS', 'INFANTIL'], n_registros),
    'acessibilidade': np.random.choice([0, 1], n_registros, p=[0.9, 0.1])
}

df = pd.DataFrame(data)
df.to_csv('teste_300_registros_seed32.csv', index=False)
print("Arquivo teste_300_registros_seed32.csv gerado com sucesso.")
