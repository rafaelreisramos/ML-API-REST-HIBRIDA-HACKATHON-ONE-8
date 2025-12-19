
import csv
import sys

input_path = r'd:\HACKATHON_API\spring_graphql_mongo\results_tests\resultado_simulacao_futura_50000_clientes (1).csv'
output_path = r'd:\HACKATHON_API\spring_graphql_mongo\test_1300_fixed.csv'

# Header expected by Java Input
# clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso

print(f"Reading {input_path}...")

count = 0
fixed_rows = []

with open(input_path, 'r', encoding='utf-8') as f_in:
    # We read manually because DictReader might be confused by the shifted columns
    lines = f_in.readlines()
    
    # header is lines[0]
    # data starts at lines[1]
    
    # Write header for output
    header = "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso"
    
    for i in range(1, len(lines)):
        if count >= 1300:
            break
            
        line = lines[i].strip()
        parts = line.split(',')
        
        # Original parts length should be 16 for input, but the bad file has output columns + extra splits
        # Bad row example: 
        # clienteId,idade,genero,regiao, 29, 90, 12, basico, ...
        # index: 0, 1, 2, 3, 4(bad), 5(bad), 6(bad), 7 ...
        
        # Heuristic fix:
        # parts[0] = Id
        # parts[1] = Idade
        # parts[2] = Genero
        # parts[3] = Regiao
        # parts[4] = "29"
        # parts[5] = "90" -> Should merge with 4 -> "29.90"
        # parts[6] = "12" -> Tempo
        # parts[7] = "basico" -> Plano
        
        # Let's reconstruct.
        # We assume the error "comma in float" happened for valorMensal (idx 4) and possibly others?
        # Let's check typical shift.
        
        # If parts[5] is numeric and parts[6] is numeric (12) and parts[7] is string (plan),
        # likely 4+5 is valor.
        
        # Let's try to reconstruct strictly the 16 fields we need for input.
        
        try:
            # Basic fields safe from comma
            c_id = parts[0]
            idade = parts[1]
            genero = parts[2]
            regiao = parts[3]
            
            # parts[4] + parts[5] -> valor
            valor_mensal = f"{parts[4]}.{parts[5]}" # 29.90
            
            # Shifted indices
            tempo = parts[6] # 12
            plano = parts[7] # basico
            metodo = parts[8] # credito
            disp = parts[9] # mobile
            viz = parts[10] # 20
            contatos = parts[11] # 0
            
            # avaliacaoPlataforma (4) -> might be 4,0 -> split?
            # In sample: "4" then "0" then "4" ...
            # sample: ...,20,0,4,0,4,0,4,0,45,1 ...
            # parts[10]=20
            # parts[11]=0 (contatos)
            # parts[12]=4 (aval plat part 1)
            # parts[13]=0 (aval plat part 2) -> "4.0"
            
            aval_plat = f"{parts[12]}.{parts[13]}"
            
            # parts[14]=4 (aval cont med part 1)
            # parts[15]=0 -> "4.0"
            aval_cont_med = f"{parts[14]}.{parts[15]}"
            
            # parts[16]=4 (aval last part 1)
            # parts[17]=0 -> "4.0"
            aval_last = f"{parts[16]}.{parts[17]}"
            
            # parts[18]=45 (tempo medio)
            tempo_sessao = parts[18]
            
            # parts[19]=1 (dias)
            dias = parts[19]
            
            # Construct line
            new_line = f"{c_id},{idade},{genero},{regiao},{valor_mensal},{tempo},{plano},{metodo},{disp},{viz},{contatos},{aval_plat},{aval_cont_med},{aval_last},{tempo_sessao},{dias}"
            
            fixed_rows.append(new_line)
            count += 1
            
        except IndexError:
            # If line is weird, skip or fill dummy? for now skip
            continue

print(f"Extracted {len(fixed_rows)} fixed rows.")

with open(output_path, 'w', encoding='utf-8') as f_out:
    f_out.write(header + "\n")
    for r in fixed_rows:
        f_out.write(r + "\n")

print("Done.")
