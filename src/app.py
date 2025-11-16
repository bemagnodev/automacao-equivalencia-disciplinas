# 1. Bibliotecas padrão (Standard Library)
import os

# 2. Bibliotecas de terceiros (Third-party)
import streamlit as st

# 3. Módulos da sua aplicação (Local application)
from components import (
    render_header,
    render_sidebar,
    render_spreadsheet_uploader,
    report_card_compact,
    load_data_from_url,
    validate_spreadsheet_data
)
from core import find_equivalencies
from data_loader import get_university_list, load_spreadsheet
from pdf_generator import create_pdf_bytes


def main():
    # --- Configuração de caminhos ---
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FAVICON_PATH = os.path.join(PROJECT_ROOT, "assets", "icon.png")
    LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "logo_ic.png")
    
    # --- Configuração da Página ---   
    st.set_page_config(
        page_title="Analisador de Equivalências",
        page_icon=FAVICON_PATH,
        layout="centered"
    )

    # --- Inicialização do Estado da Aplicação ---
    if 'spreadsheet_data' not in st.session_state:
        st.session_state.spreadsheet_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []

    # --- Renderização dos Componentes Visuais Estáticos ---
    render_sidebar()
    render_header(LOGO_PATH)

    # --- ETAPA 1: CARREGAMENTO E VALIDAÇÃO DOS DADOS (DA URL) ---
    
    # Só executa a carga e validação se os dados AINDA NÃO estiverem na sessão
    if st.session_state.spreadsheet_data is None: 
        with st.spinner("Carregando e validando planilha de equivalências..."):
            
            # 1. Tenta carregar os dados (da URL do .env)
            load_error, data = load_data_from_url()

            if load_error:
                st.error(load_error)
                st.stop()  # Para a execução do app se o carregamento falhar
            
            # 2. Tenta validar os dados (se o carregamento foi OK)
            is_valid, validation_message = validate_spreadsheet_data(data)

            if not is_valid:
                st.error(validation_message)
                st.stop()  # Para a execução se a validação falhar

            # 3. Sucesso! Armazena os dados na sessão
            st.session_state.spreadsheet_data = data
            st.session_state.analysis_results = [] # Reseta os resultados

    
    # --- ETAPA 2 e 3: SELEÇÃO DA UNIVERSIDADE E ENTRADA DOS CÓDIGOS ---

    #TODO botar nome aluno

    # Esta lógica permanece a mesma. 
    # Ela só vai rodar se a 'ETAPA 1' for bem-sucedida.
    if st.session_state.spreadsheet_data:
        st.subheader("Selecione a Universidade e Insira os Códigos")
        
        col1, col2 = st.columns([1, 2])
        
        #TODO testar visualização em colunas
        with col1:
            st.markdown("**Universidade de Origem**")
            university_list = get_university_list(st.session_state.spreadsheet_data)
            selected_university = st.selectbox(
                "Universidade de Origem",
                options=university_list,
                label_visibility="collapsed" 
            )

        with col2:
            st.markdown("**Códigos das Disciplinas de Origem**")
            course_codes_input = st.text_area(
                "Códigos das Disciplinas de Origem",
                height=150,
                label_visibility="collapsed"  
            )
            st.caption("Separe os códigos por espaço, vírgula ou quebra de linha.")

    # --- ETAPA 4: BOTÃO DE ANÁLISE ---
        if st.button("Analisar Equivalências", type="primary", use_container_width=True):
            if course_codes_input.strip():
                with st.spinner("Buscando equivalências..."):
                    st.session_state.analysis_results = find_equivalencies(
                        st.session_state.spreadsheet_data,
                        selected_university,
                        course_codes_input
                    )
            else:
                st.warning("Por favor, insira pelo menos um código de disciplina para analisar.")

    # --- ETAPA 5: EXIBIÇÃO DOS RESULTADOS ---
    if st.session_state.analysis_results:
        st.markdown("---")
         
        has_not_found = report_card_compact(st.session_state.analysis_results)

        st.markdown("---")

        # --- ETAPA 6: GERAÇÃO DO PDF (CONDICIONAL) ---
        if not has_not_found:
            st.subheader("Gerar Relatório")
            st.success("Todas as disciplinas foram encontradas! Você já pode gerar o relatório.")

            pdf_bytes = create_pdf_bytes(st.session_state.analysis_results, LOGO_PATH)
            st.download_button(
                label="Baixar Relatório em PDF",
                data=pdf_bytes,
                file_name="relatorio_equivalencia.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        else:
            st.error("⚠️ **Atenção:** Algumas disciplinas não foram encontradas na planilha. O relatório final não pode ser gerado até que todas as disciplinas sejam verificadas manualmente ou os códigos corrigidos.")


if __name__ == "__main__":
    main()
