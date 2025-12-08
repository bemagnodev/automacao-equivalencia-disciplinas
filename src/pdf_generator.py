# 1. Bibliotecas padrão (Standard Library)
import os
from typing import List, Dict

# 2. Bibliotecas de terceiros (Third-party)
from fpdf import FPDF

# --- Constantes de Layout ---
PAGE_WIDTH = 297
MARGIN = 10
USABLE_WIDTH = PAGE_WIDTH - (2 * MARGIN)

COL_WIDTHS = {
    "dest_code": 25,
    "dest_name": 80,
    "origin_code": 25,
    "origin_name": 80,
    "parecer": 25,
    "justificativa": 42
}
BASE_LINE_HEIGHT = 5 
CELL_PADDING = 2

class CustomPDF(FPDF):
    """
    Classe customizada do FPDF para criar o cabeçalho e rodapé padronizados.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_path = None
        self.set_margins(MARGIN, MARGIN, MARGIN)

    def header(self):
        # --- 1. Cabeçalho Oficial (Logo e Texto) ---
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, self.l_margin, 8, 30)

        x_after_logo = self.l_margin + 30 + 5
        self.set_xy(x_after_logo, 8)
        
        self.set_font("Arial", "B", 10)
        self.cell(0, 5, "UNIVERSIDADE FEDERAL DO RIO DE JANEIRO", 0, 1, "L")
        self.set_x(x_after_logo)
        self.cell(0, 5, "Centro de Ciências Matemáticas e da Natureza", 0, 1, "L")
        self.set_x(x_after_logo)
        self.cell(0, 5, "Instituto de Computação", 0, 1, "L")
        
        # --- 2. Título do Documento ---
        self.set_font("Arial", "B", 16)
        self.ln(10)
        self.cell(0, 10, "Parecer de Análise de Equivalência de Disciplinas", 0, 1, "C")
        self.ln(5)

        # --- 3. Cabeçalho da Tabela ---
        self.set_font("Arial", "B", 9)
        self.set_fill_color(230, 230, 230)
        self.set_text_color(0, 0, 0)
        
        w_dest = COL_WIDTHS["dest_code"] + COL_WIDTHS["dest_name"]
        w_orig = COL_WIDTHS["origin_code"] + COL_WIDTHS["origin_name"]
        w_analise = COL_WIDTHS["parecer"] + COL_WIDTHS["justificativa"] 
        
        self.cell(w_dest, BASE_LINE_HEIGHT, "Disciplinas a Serem Dispensadas no IC/UFRJ", 1, 0, "C", fill=True)
        self.cell(w_orig, BASE_LINE_HEIGHT, "Disciplinas Cursadas na IES de Origem", 1, 0, "C", fill=True)
        self.cell(w_analise, BASE_LINE_HEIGHT, "Análise de Equivalência", 1, 1, "C", fill=True) 

        # Títulos das colunas (6 colunas)
        self.cell(COL_WIDTHS["dest_code"], BASE_LINE_HEIGHT, "Código", 1, 0, "C", fill=True)
        self.cell(COL_WIDTHS["dest_name"], BASE_LINE_HEIGHT, "Nome", 1, 0, "C", fill=True)
        self.cell(COL_WIDTHS["origin_code"], BASE_LINE_HEIGHT, "Código", 1, 0, "C", fill=True)
        self.cell(COL_WIDTHS["origin_name"], BASE_LINE_HEIGHT, "Nome", 1, 0, "C", fill=True)
        self.cell(COL_WIDTHS["parecer"], BASE_LINE_HEIGHT, "Parecer", 1, 0, "C", fill=True)
        self.cell(COL_WIDTHS["justificativa"], BASE_LINE_HEIGHT, "Justificativa", 1, 1, "C", fill=True) 

    def _calculate_row_height(self, row_data: Dict) -> int:
        """
        CALCULA a altura máxima necessária para a linha, ANTES de desenhá-la.
        """
        is_equivalent_str = str(row_data.get("is_equivalent", "Não")).lower()
        is_equivalent = is_equivalent_str in ['sim', 's', 'true', '1', 'verdadeiro']
        parecer_text = "Favorável" if is_equivalent else "Desfavorável"
        
        justification_text = row_data.get("justification") or ""

        # --- CORREÇÃO APLICADA AQUI ---
        # Garantir que tudo seja string antes de passar para o PDF
        cell_texts = [
            str(row_data.get("dest_codes") or ""),
            str(row_data.get("dest_names") or ""),
            str(row_data.get("origin_codes") or ""),
            str(row_data.get("origin_names") or ""),
            str(parecer_text),
            str(justification_text)
        ]
        # --- FIM DA CORREÇÃO ---
        
        cell_widths = [
            COL_WIDTHS["dest_code"],
            COL_WIDTHS["dest_name"],
            COL_WIDTHS["origin_code"],
            COL_WIDTHS["origin_name"],
            COL_WIDTHS["parecer"],
            COL_WIDTHS["justificativa"]
        ]
        
        max_lines = 1
        self.set_font("Arial", "", 8)

        for i in range(len(cell_texts)):
            text = cell_texts[i] # Agora é garantido que 'text' é uma string
            width = cell_widths[i] - (CELL_PADDING * 2)
            
            if width <= 0: continue
            
            lines = self.multi_cell(
                width, 
                BASE_LINE_HEIGHT, 
                text, 
                border=0,
                align="L", 
                split_only=True
            )
            max_lines = max(max_lines, len(lines))

        return (max_lines * BASE_LINE_HEIGHT) + (CELL_PADDING / 2)

    def print_table_row(self, row_data: Dict):
        """
        Imprime uma linha da tabela, usando a altura pré-calculada.
        """
        self.set_font("Arial", "", 8)
        self.set_text_color(0, 0, 0)
        
        total_row_height = self._calculate_row_height(row_data)
        
        # --- Prepara os textos ---
        is_equivalent_str = str(row_data.get("is_equivalent", "Não")).lower()
        is_equivalent = is_equivalent_str in ['sim', 's', 'true', '1', 'verdadeiro']
        parecer_text = "Favorável" if is_equivalent else "Desfavorável"
        
        justification_text = row_data.get("justification") or ""

        # --- CORREÇÃO APLICADA AQUI ---
        # Garantir que tudo seja string antes de passar para o PDF
        cell_texts = [
            str(row_data.get("dest_codes") or ""),
            str(row_data.get("dest_names") or ""),
            str(row_data.get("origin_codes") or ""),
            str(row_data.get("origin_names") or ""),
            str(parecer_text),
            str(justification_text)
        ]
        # --- FIM DA CORREÇÃO ---
        
        cell_widths = [
            COL_WIDTHS["dest_code"],
            COL_WIDTHS["dest_name"],
            COL_WIDTHS["origin_code"],
            COL_WIDTHS["origin_name"],
            COL_WIDTHS["parecer"],
            COL_WIDTHS["justificativa"]
        ]
        
        start_y = self.get_y()
        current_x = self.l_margin
        
        for i in range(len(cell_texts)):
            width = cell_widths[i]
            text = cell_texts[i] # Agora é garantido que 'text' é uma string
            
            self.set_xy(current_x, start_y) 
            
            self.multi_cell(
                width, 
                total_row_height,
                text, 
                border=1, 
                align="L",
                new_x="RIGHT",
                new_y="TOP"
            )
            current_x += width
            
        self.set_y(start_y + total_row_height)

# --- Função Principal (a ser chamada pelo app.py) ---

def create_pdf_bytes(results: list, logo_path: str) -> bytes:
    """
    Gera o conteúdo de um relatório em PDF como um objeto de bytes,
    com cabeçalho oficial e tabela formatada.
    """
    found_results = [r for r in results if r.get("status") == "Encontrado"]

    if not found_results:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Nenhum resultado encontrado para gerar o relatório.", 0, 1, "C")
        return bytes(pdf.output())

    pdf = CustomPDF(orientation="L", unit="mm", format="A4")
    pdf.logo_path = logo_path
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    for item in found_results:
        pdf.print_table_row(item)

    return bytes(pdf.output())


if __name__ == "__main__":
    # --- Bloco de Teste ---
    print("Iniciando teste de geração de PDF...")

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    LOGO_TO_TEST = os.path.join(PROJECT_ROOT, "assets", "logo_ic.png")
    
    if not os.path.exists(LOGO_TO_TEST):
        print(f"AVISO: Logo de teste não encontrado em '{LOGO_TO_TEST}'. O cabeçalho ficará incompleto.")
        LOGO_TO_TEST = None

    sample_results_for_test = [
        {"input_code": "CEX001", "status": "Encontrado", "origin_codes": "CEX001", "origin_names": "Cálculo I", "is_equivalent": "Sim", "dest_codes": "MAC118", "dest_names": "Cálculo Diferencial e Integral I", "justification": "Ementa e carga horária totalmente compatíveis."},
        {"input_code": "FIS002", "status": "Encontrado", "origin_codes": "FIS002", "origin_names": "Física Experimental I", "is_equivalent": "Não", "dest_codes": "FIS121", "dest_names": "Física Experimental I", "justification": "Carga horária insuficiente."},
        {"input_code": "COMP123", "status": "Não Encontrado na Planilha"},
        {"input_code": "QUI003", "status": "Encontrado", "origin_codes": "QUI003 + QUI004", "origin_names": "Química Geral e Inorgânica", "is_equivalent": True, "dest_codes": "QUIG11", "dest_names": "Química Geral", "justification": None}, # Teste com Nulo
        {"input_code": "ENG123", "status": "Encontrado", "origin_codes": 12345, "origin_names": "Engenharia de Software", "is_equivalent": True, "dest_codes": 54321, "dest_names": "Engenharia de Software I", "justification": "OK."} # <-- TESTE COM 'int'
    ]

    pdf_bytes = create_pdf_bytes(sample_results_for_test, LOGO_TO_TEST)

    if pdf_bytes:
        file_path = "teste_relatorio_corrigido_final.pdf"
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ PDF de teste gerado com sucesso!")
        print(f"Abra o arquivo '{file_path}' para verificar o resultado.")
    else:
        print("❌ Nenhum dado encontrado para gerar o PDF.")