import requests
import json

URL = "http://localhost:5000/predict"

def test_prediction(cenario_nome, dados, espera_churn):
    print(f"\n🧪 Testando Cenário: {cenario_nome}")
    print(f"Dados Relevantes: Sessão={dados['tempoMedioSessaoMin']}min, Avaliação={dados['avaliacaoConteudoUltimoMes']}, DiasSemAcesso={dados['diasUltimoAcesso']}")
    
    try:
        response = requests.post(URL, json=dados)
        response.raise_for_status()
        result = response.json()
        
        prob = result['probabilidade']
        previsao = result['previsao']
        
        print(f"🔍 Resultado Modelo: Probabilidade={prob:.4f} | Previsão='{previsao}'")
        
        passou = False
        if espera_churn and prob > 0.4287:
            print("✅ SUCESSO: Modelo previu CHURN corretamente (Prob alta).")
            passou = True
        elif not espera_churn and prob < 0.4287:
            print("✅ SUCESSO: Modelo previu CONTINUIDADE corretamente (Prob baixa).")
            passou = True
        else:
            print("❌ FALHA: O modelo não seguiu a lógica esperada para este perfil!")
            
        return passou
            
    except Exception as e:
        print(f"🔥 Erro na requisição: {e}")
        return False

# --- CASO 1: Cliente "Perfeito" (Engajado) ---
# Baseado nas features top: Sessão longa (28% peso), Avaliação alta, Uso recente.
cliente_fiel = {
    "idade": 30,
    "tempoAssinaturaMeses": 24,
    "planoAssinatura": "Premium",
    "valorMensal": 59.90,
    "visualizacoesMes": 50,
    "contatosSuporte": 0,
    "metodoPagamento": "Cartão de Crédito",
    "dispositivoPrincipal": "Smart TV",
    "avaliacaoConteudoMedia": 5.0,
    "avaliacaoConteudoUltimoMes": 5.0, # Feature top 3
    "tempoMedioSessaoMin": 120,        # Feature top 1 (Sessão longa)
    "diasUltimoAcesso": 0,             # Feature top recência
    "avaliacaoPlataforma": 5.0,
    "regiao": "Sudeste",
    "genero": "Feminino",
    "tipoContrato": "Anual",
    "categoriaFavorita": "Filmes",
    "acessibilidade": 0
}

# --- CASO 2: Cliente em Risco (Desengajado) ---
# Sessão curta, Avaliação baixa, Dias sem acesso.
cliente_risco = {
    "idade": 30,
    "tempoAssinaturaMeses": 2,
    "planoAssinatura": "Básico",
    "valorMensal": 29.90,
    "visualizacoesMes": 2,
    "contatosSuporte": 5,
    "metodoPagamento": "Boleto",
    "dispositivoPrincipal": "Mobile",
    "avaliacaoConteudoMedia": 2.0,
    "avaliacaoConteudoUltimoMes": 1.0, # Baixa avaliação
    "tempoMedioSessaoMin": 5,          # Sessão curtíssima (Risco)
    "diasUltimoAcesso": 25,            # Inativo há quase um mês
    "avaliacaoPlataforma": 2.0,
    "regiao": "Norte",
    "genero": "Masculino",
    "tipoContrato": "Mensal",
    "categoriaFavorita": "Nenhuma",
    "acessibilidade": 0
}

print("="*60)
print("🧐 VALIDANDO COMPORTAMENTO DO MODELO (AI-SERVICE)")
print("="*60)

r1 = test_prediction("CLIENTE FIEL (Engajado)", cliente_fiel, espera_churn=False)
r2 = test_prediction("CLIENTE DE RISCO (Desengajado)", cliente_risco, espera_churn=True)

print("\n"+"="*60)
if r1 and r2:
    print("🏆 CONCLUSÃO: O serviço de IA está consistente com o modelo treinado!")
    print("   Ele reage corretamente aos fatores de peso (tempo de sessão, avaliação).")
    print("   Podemos confiar nos resultados.")
else:
    print("⚠️ CONCLUSÃO: O modelo apresentou inconsistências. Verificar preprocessing.")
print("="*60)
