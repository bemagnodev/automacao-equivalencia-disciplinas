import os
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv
import streamlit as st
from typing import Tuple, Dict, Optional
from data_loader import load_spreadsheet 


REQUIRED_COLUMNS = {
    "Códigos Origem",
    "Nomes Origem",
    "Equivalente?",
    "Códigos UFRJ Destino",
    "Nomes UFRJ Destino",
    "Justificativa Parecer"
}


def validate_spreadsheet(uploaded_file) -> tuple[bool, str]:
    """
    Valida a planilha carregada, verificando se PELO MENOS UMA aba 
    contém as colunas necessárias (definidas em REQUIRED_COLUMNS).

    Args:
        uploaded_file: O objeto de arquivo carregado pelo Streamlit.

    Returns:
        tuple[bool, str]: Uma tupla contendo (True/False para validade, mensagem de status).
    """
    if uploaded_file is None:
        return False, "Nenhum arquivo carregado."

    spreadsheet_data = load_spreadsheet(uploaded_file)
    
    if spreadsheet_data is None:
        return False, "O arquivo não pôde ser lido. Verifique se é um arquivo .xlsx válido."
    
    # Se o dict de planilhas estiver vazio (arquivo sem abas)
    if not spreadsheet_data:
         return False, "O arquivo .xlsx está vazio (não contém abas)."

    # Itera pelas abas procurando por PELO MENOS UMA válida
    for sheet_name, df in spreadsheet_data.items():
        sheet_columns = set(df.columns)
        
        # Se as colunas obrigatórias SÃO um subconjunto das colunas da aba
        if REQUIRED_COLUMNS.issubset(sheet_columns):
            # Encontrou uma aba válida, a planilha inteira é considerada válida
            return True, "Planilha validada: Pelo menos uma aba de faculdade válida foi encontrada."
            
    # Se o loop terminar, significa que NENHUMA aba válida foi encontrada
    error_message = (
        "Validação falhou! Nenhuma aba na planilha contém o conjunto completo de colunas obrigatórias. "
        f"Verifique se pelo menos uma aba possui: {', '.join(list(REQUIRED_COLUMNS))}"
    )
    return False, error_message


def render_spreadsheet_uploader():
    """
    Renderiza o componente de upload de arquivo e realiza a validação da planilha.

    Returns:
        O objeto do arquivo carregado (UploadedFile) se for válido, senão None.
    """
    st.subheader("1. Carregue a Planilha de Equivalências")
    uploaded_file = st.file_uploader(
        "Selecione o arquivo .xlsx com os dados de equivalência",
        type="xlsx",
        label_visibility="collapsed"
    )

    if uploaded_file:
        is_valid, message = validate_spreadsheet(uploaded_file)
        if is_valid:
            st.success(message)
            return uploaded_file
        else:
            st.error(message)
            return None
            
    return None

# Novas funcoes

def validate_spreadsheet_data(spreadsheet_data: dict[str, DataFrame]) -> tuple[bool, str]:
    """
    Valida um DICIONÁRIO de dados de planilha já carregado.
    
    Verifica se PELO MENOS UMA aba (DataFrame) no dicionário 
    contém as colunas obrigatórias.

    Args:
        spreadsheet_data (dict[str, DataFrame]): O dicionário de dados carregado.

    Returns:
        tuple[bool, str]: (is_valid, status_message)
    """
    if not spreadsheet_data:
         return False, "Os dados da planilha estão vazios (não contêm abas)."

    # Verifica se 'QUALQUER' (any) valor de DataFrame (df.columns) no dicionário atende à condição.
    is_valid = any(
        REQUIRED_COLUMNS.issubset(df.columns) 
        for df in spreadsheet_data.values()
    )

    if is_valid:
        return True, "Validação bem-sucedida: Pelo menos uma aba válida foi encontrada."
    else:
        error_message = (
            "Validação falhou! Nenhuma aba na planilha contém o conjunto completo "
            f"de colunas obrigatórias: {', '.join(list(REQUIRED_COLUMNS))}"
        )
        return False, error_message


@st.cache_data(ttl=600) # Cache de 10 minutos
def load_data_from_url() -> Tuple[Optional[str], Optional[Dict[str, DataFrame]]]:
    """
    Carrega uma planilha PÚBLICA (.xlsx) de uma URL do .env.
    Lê TODAS as abas do arquivo Excel.

    Retorna:
        Tuple[Optional[str], Optional[Dict[str, DataFrame]]]:
        (error_message, data_dict)
        - (None, data_dict) em caso de sucesso.
        - (error_message, None) em caso de falha.
    """
    load_dotenv()
    
    sheet_url = os.getenv("PUBLIC_EXCEL_URL")
    
    if not sheet_url:
        msg = "Configuração incompleta: 'PUBLIC_EXCEL_URL' não está definida no seu arquivo .env."
        return msg, None

    try:
        # sheet_name=None carrega todas as abas em um dicionário
        spreadsheet_data = pd.read_excel(
            sheet_url, 
            sheet_name=None, 
            engine='openpyxl' # Requer que 'openpyxl' esteja instalado
        )
        
        if not spreadsheet_data:
             return "Planilha carregada, mas está vazia (não contém abas).", None
        
        # Sucesso
        return None, spreadsheet_data
        
    except Exception as e:
        error_msg = (
            f"Erro ao carregar a planilha da URL. Verifique o link no .env e se o "
            f"arquivo é um .xlsx válido. (Erro: {e})"
        )
        return error_msg, None
