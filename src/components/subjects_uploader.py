import streamlit as st
import pandas as pd
import camelot
import tempfile
import os
import re
from typing import Any, List

# --- 1. Lógica de Backend ---

def _scrape_pdf_content(uploaded_file: Any) -> List[pd.DataFrame]:
    """
    Roda o Camelot e retorna a lista de DataFrames.
    """
    extracted_dfs = []
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tfile:
            tfile.write(uploaded_file.getvalue())
            temp_path = tfile.name

        # Parâmetros de tolerância (script do seu colega)
        tables = camelot.read_pdf(
            temp_path, 
            pages='all', 
            flavor='stream',
            strip_text='\n',
            edge_tol=500,
            row_tol=15,
            column_tol=10
        )

        for table in tables:
            extracted_dfs.append(table.df)

    except Exception as e:
        st.error(f"Erro no Camelot: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    return extracted_dfs

def _extract_clean_codes(dfs: List[pd.DataFrame]) -> str:
    """
    Pega a 2ª tabela e usa REGEX para manter APENAS códigos (Ex: MAE111).
    Retorna os códigos separados por QUEBRA DE LINHA (\n).
    """
    if not dfs or len(dfs) < 2:
        return ""

    # Foco na SEGUNDA tabela (índice 1)
    target_df = dfs[1]
    
    # Pega todos os dados da terceira coluna como lista de strings
    raw_data = target_df.iloc[:, 2].astype(str).tolist()
    
    clean_codes = []
    pattern = re.compile(r'[A-Z]{3}\d{3}') # Regex: 3 Letras + 3 Números

    for item in raw_data:
        match = pattern.search(item)
        if match:
            clean_codes.append(match.group())
            
        # matches = pattern.findall(item)
        # clean_codes.extend(matches) # Adiciona todos que achou
            
    return "\n".join(clean_codes)

# --- 2. O Componente de Interface ---

def render_subject_uploader():
    """
    Renderiza o uploader e retorna o texto final.
    """
    WIDGET_KEY = "codes_input_area"
    
    st.markdown("**Códigos das Disciplinas de Origem**")

    uploaded_file = st.file_uploader(
        "Carregar PDF", 
        type=["pdf"], 
        key="pdf_uploader_component",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # Só processa se for um arquivo novo
        if "last_processed_id" not in st.session_state or st.session_state["last_processed_id"] != file_id:
            
            with st.spinner("Extraindo códigos..."):
                dfs = _scrape_pdf_content(uploaded_file)
                clean_text = _extract_clean_codes(dfs)
                
                if clean_text:
                    # Atualiza o widget text_area
                    st.session_state[WIDGET_KEY] = clean_text
                    st.toast("Códigos extraídos!", icon="✨")
                else:
                    st.warning("Nenhum código encontrado na 2ª tabela.")
            
            st.session_state["last_processed_id"] = file_id

    # Widget de Texto
    final_input = st.text_area(
        "Códigos extraídos",
        height=300, # Aumentei um pouco a altura para caber a lista vertical
        key=WIDGET_KEY,
        placeholder="Faça upload do PDF ou digite os códigos aqui...",
        help="Um código por linha."
    )
    
    st.caption("Formato: AAA000 (um por linha).")

    return final_input

# --- 3. Teste Isolado (Com 2 Colunas) ---
if __name__ == "__main__":
    st.set_page_config(layout="wide") # Layout wide fica melhor com colunas
    
    st.title("Teste: Layout de Colunas + Quebra de Linha")

    # --- Simulando sua Main ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Esta coluna está vazia (ou com outras infos), como na sua main.")
        st.image("https://placehold.co/400x300?text=Espaço+Reservado", caption="Placeholder")

    with col2:
        # Chama o componente na coluna 2
        resultado = render_subject_uploader()

    # Mostra o resultado final fora das colunas para conferência
    if resultado:
        st.divider()
        st.write("Dado final que será usado no script:")
        st.text(resultado) # st.text preserva a quebra de linha visualmente