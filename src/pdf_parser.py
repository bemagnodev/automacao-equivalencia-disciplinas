import pdfplumber
import re
from pprint import pprint

def find_value(text, pattern):
    """
    Busca um valor no texto usando regex e retorna o grupo 1.
    """
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

def parse_equivalencia_pdf(pdf_path):
    """
    Analisa o PDF de requerimento de equivalência e extrai os dados.
    Esta versão é robusta para PDFs "achatados" (não-formulário).
    """
    student_data = {
        "name": None,
        "email": None,
        "dre": None,
        "date": None,
        "origin_institution": None,
        "disciplines": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            
            # --- Página 1: Dados Pessoais  ---
            if len(pdf.pages) > 0:
                page_01 = pdf.pages[0]
                text_01 = page_01.extract_text()

                student_data['name'] = find_value(text_01, r"NOME:\s*\n\s*([^\n]+)")
                student_data['dre'] = find_value(text_01, r"DRE:\s*\n\s*([^\n]+)")
                student_data['email'] = find_value(text_01, r"EMAIL:\s*([^\s]+)")
                student_data['date'] = find_value(text_01, r"DATA:\s*(\d{2}/\d{2}/\d{4})")
                student_data['origin_institution'] = find_value(text_01, r"INSTITUIÇÃO DE ENSINO SUPERIOR:\s*([^\n]+)")

            # --- Página 2: Tabela (Lógica Manual) ---
            if len(pdf.pages) > 1:
                page_02 = pdf.pages[1]
                text_02 = page_02.extract_text(layout=True)
                lines = text_02.split('\n')
                
                disciplines_list = []
                data_lines = lines
                
                # Regex para as linhas principais da tabela
                # \s{2,} (dois ou mais espaços) é o que divide as colunas
                simple_line_regex = re.compile(
                    r'^((?:ICP|MAE)\d{3})\s+(.+?)\s{2,}((?:MAT|INF|CTC)\d{3,})\s+(.+?)\s+(\d{4})$'
                )
                complex_line_regex = re.compile(
                    r'^((?:ICP|MAE)\d{3})\s+(.+?)\s{2,}(.+?)\s+(\d{4})$'
                )
                
                # --- [A LÓGICA FINAL] ---
                # Em vez de loops 'while', iteramos linha por linha.
                # Se uma linha é "principal", ela é responsável por
                # verificar suas linhas vizinhas (i-1 e i+1).

                # Usamos um 'set' para rastrear as linhas "fragmento"
                # que já foram usadas por uma linha principal.
                processed_fragments = set()

                for i, line in enumerate(data_lines):
                    line = line.strip()
                    if not line or i in processed_fragments:
                        continue

                    # CASO 1: Linha simples (Tudo nela)
                    simple_match = simple_line_regex.match(line)
                    if simple_match:
                        disciplines_list.append({
                            "ufrj_discipline": {
                                "code": simple_match.group(1).strip(),
                                "name": simple_match.group(2).strip()
                            },
                            "origin_discipline": {
                                "code": simple_match.group(3).strip(),
                                "name": simple_match.group(4).strip()
                            }
                        })
                        continue

                    # CASO 2: Linha complexa (Código em outras linhas)
                    complex_match = complex_line_regex.match(line)
                    if complex_match:
                        ufrj_code = complex_match.group(1).strip()
                        ufrj_name = complex_match.group(2).strip()
                        origin_name = complex_match.group(3).strip()
                        origin_code_parts = []

                        # Olha 1 linha para TRÁS
                        if i > 0:
                            prev_line = data_lines[i-1].strip()
                            # Se a linha anterior não for vazia e não for uma linha principal
                            if prev_line and not simple_line_regex.match(prev_line) and not complex_line_regex.match(prev_line):
                                origin_code_parts.append(prev_line)
                                processed_fragments.add(i-1)

                        # Olha 1 linha para FRENTE
                        if i + 1 < len(data_lines):
                            next_line = data_lines[i+1].strip()
                            # Se a linha seguinte não for vazia e não for uma linha principal
                            if next_line and not simple_line_regex.match(next_line) and not complex_line_regex.match(next_line):
                                origin_code_parts.append(next_line)
                                processed_fragments.add(i+1)
                        
                        disciplines_list.append({
                            "ufrj_discipline": {"code": ufrj_code, "name": ufrj_name},
                            "origin_discipline": {
                                "code": " ".join(origin_code_parts),
                                "name": origin_name
                            }
                        })
                        
                student_data['disciplines'] = disciplines_list

    except Exception as e:
        print(f"Erro ao processar o PDF {pdf_path}: {e}")
        return None

    return student_data

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    file_name = "data/requerimento_equivalencias.pdf"
    
    print(f"Iniciando extração do arquivo: {file_name}\n")
    data = parse_equivalencia_pdf(file_name)
    
    if data:
        print("--- Dados Extraídos ---")
        pprint(data)
        print("\nExtração concluída.")
    else:
        print("Não foi possível extrair os dados.")