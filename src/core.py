import pandas as pd

def find_equivalencies(
    all_data: dict[str, pd.DataFrame], 
    selected_university: str, 
    course_codes_str: str
) -> list[dict]:
    
    results = []
    
    university_df = all_data.get(selected_university)
    if university_df is None:
        return [{"error": f"Dados para a universidade '{selected_university}' não encontrados."}]

    # --- CORREÇÃO 1: Limpeza da Entrada (Input do Usuário) ---
    # Substituímos '+' por espaço para garantir que "INF01+INF02" vire {"INF01", "INF02"}
    # Isso resolve o caso se o usuário colar direto com o +.
    cleaned_str = course_codes_str.replace("+", " ").replace(",", " ").replace("\n", " ")
    
    # Set de códigos do usuário (Input)
    input_codes_set = {code.strip().upper() for code in cleaned_str.split() if code.strip()}

    # --- CORREÇÃO 2: Prioridade de Regras (Sort by Complexity) ---
    # Criamos uma cópia para não bagunçar o original
    df_sorted = university_df.copy()
    
    # Criamos uma coluna temporária para medir o tamanho da regra.
    # Regras como "INF01+INF02" são mais longas que "INF01".
    # Queremos processar as MAIORES primeiro.
    df_sorted['complexity'] = df_sorted['Códigos Origem'].astype(str).apply(len)
    
    # Ordena do maior para o menor (Regras compostas vêm pro topo)
    df_sorted = df_sorted.sort_values(by='complexity', ascending=False)

    # Itera sobre as regras ordenadas
    for index, rule in df_sorted.iterrows():
        origin_codes_str = str(rule['Códigos Origem'])
        
        # --- CORREÇÃO 3: Parse da Regra da Planilha ---
        # Quebra a regra "INF1+INF2" em um conjunto {"INF1", "INF2"}
        required_codes = {c.strip().upper() for c in origin_codes_str.split('+') if c.strip()}
        
        # Lógica: O usuário tem TODOS os códigos exigidos por essa regra?
        if required_codes and required_codes.issubset(input_codes_set):
            # CASAMENTO PERFEITO!
            result_details = {
                "status": "Encontrado",
                "origin_codes": rule['Códigos Origem'],
                "origin_names": rule['Nomes Origem'],
                "is_equivalent": rule['Equivalente?'],
                "dest_codes": rule['Códigos UFRJ Destino'],
                "dest_names": rule['Nomes UFRJ Destino'],
                "justification": rule['Justificativa Parecer']
            }
            results.append(result_details)
            
            # Remove os códigos usados do "bolso" do usuário para não serem reusados
            input_codes_set -= required_codes

    # Sobras: Códigos que o usuário tem, mas não serviram para nenhuma regra
    for remaining_code in sorted(list(input_codes_set)):
        results.append({
            "input_code": remaining_code,
            "status": "Não Encontrado na Planilha"
        })

    return results