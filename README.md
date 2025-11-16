# Analisador de Equivalência de Disciplinas

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?style=for-the-badge&logo=pandas)

## 🎯 Sobre o Projeto

O **Analisador de Equivalência de Disciplinas** é uma ferramenta interativa projetada para simplificar e agilizar a consulta de regras de equivalência entre diferentes universidades ou currículos.

A aplicação permite que coordenadores, administradores ou alunos carreguem uma planilha centralizada contendo todas as regras de equivalência. Com base nesses dados, os usuários podem selecionar uma universidade de origem, inserir uma lista de códigos de disciplinas e instantaneamente descobrir suas equivalentes, gerando um relatório formal em PDF ao final do processo.

O objetivo é substituir a busca manual em documentos e planilhas complexas por uma interface web rápida, intuitiva e à prova de erros.

## ✨ Funcionalidades Principais

-   **Base de Dados Flexível:** Faça o upload de uma planilha (`.xlsx`, `.csv`) com as regras de equivalência, permitindo que a ferramenta se adapte a qualquer instituição.
-   **Consulta Dinâmica:** Selecione a universidade e insira múltiplos códigos de disciplina para análise simultânea.
-   **Resultados Imediatos:** A lógica de busca exibe os resultados da equivalência diretamente na tela.
-   **Geração de Relatório:** Exporte um relatório limpo e profissional em formato `.pdf` com os resultados da análise.
-   **Interface Simples e Direta:** Construído com Streamlit para uma experiência de usuário limpa e focada na tarefa.

## ⚙️ Como Usar a Ferramenta

O fluxo de trabalho é dividido em etapas claras na própria interface:

1.  **Carregue a Planilha de Regras:**
    -   Na seção "1. Faça o Upload da Planilha de Equivalências", clique em "Procurar arquivos".
    -   Selecione a planilha (`.xlsx` ou `.csv`) que contém a base de dados com as regras. A aplicação irá carregá-la e prepará-la para a consulta.

2.  **Selecione a Universidade e Insira os Códigos:**
    -   Na seção "2. Selecione a Universidade e Insira os Códigos", escolha a **Universidade de Origem** na lista suspensa.
    -   No campo de texto ao lado, digite ou cole os **códigos das disciplinas** que deseja analisar. Você pode separá-los por espaço, vírgula ou quebra de linha.

3.  **Analise e Veja o Resultado:**
    -   Clique no botão **"Analisar Equivalências"**.
    -   O sistema buscará as correspondências na planilha e exibirá os resultados logo abaixo.

4.  **Baixe o Relatório em PDF:**
    -   Se todas as disciplinas inseridas forem encontradas, um botão **"Baixar Relatório em PDF"** aparecerá.
    -   Clique nele para salvar um documento formal com os resultados da sua consulta.

## 🛠️ Para Desenvolvedores (Estrutura do Projeto)

O projeto é modularizado para facilitar a manutenção e escalabilidade.

-   `main.py`: Ponto de entrada da aplicação Streamlit. Orquestra o fluxo da interface, gerencia o estado da sessão (`st.session_state`) e chama os outros módulos.
-   `/components`: Contém os módulos responsáveis por renderizar partes específicas da UI (cabeçalho, barra lateral, uploader de arquivos, etc.), mantendo o `main.py` mais limpo.
-   `data_loader.py`: Funções para carregar, validar e pré-processar a planilha de regras enviada pelo usuário.
-   `core.py`: Abriga a lógica principal da aplicação, incluindo a função `find_equivalencies` que realiza a busca pelas equivalências na base de dados.
-   `pdf_generator.py`: Responsável por pegar os resultados da análise e criar um documento PDF para download.
-   `/assets`: Armazena arquivos estáticos como o ícone (`favicon`) e o logo da aplicação.

### Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://URL_DO_SEU_REPOSITORIO.git
    cd nome-do-diretorio
    ```

2.  **Crie um ambiente virtual e ative-o:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS / Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run main.py
    ```

5.  Acesse `http://localhost:8501` no seu navegador.