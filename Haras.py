import streamlit as st
from playwright.sync_api import sync_playwright
from datetime import datetime

# Função para rodar a automação com Playwright
def executar_automacao(data_inicio, data_fim):
    with sync_playwright() as p:
        # Inicializa o navegador no modo headless (sem interface gráfica)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Acessa o site
        page.goto("https://portal.minhaagendaapp.com.br/agenda")

        # Preenche login e senha
        page.fill("input[type='email']", st.secrets["email"])
        page.fill("input[type='password']", st.secrets["senha"])
        page.press("input[type='password']", "Enter")

        # Aguarda a página carregar
        page.wait_for_selector("button.MuiButtonBase-root")

        # Passo 1: Clica no botão "Exportar"
        try:
            botao_exportar = page.query_selector("button.MuiButtonBase-root.MuiIconButton-root")
            botao_exportar.scroll_into_view_if_needed()
            botao_exportar.click()
            st.success("✅ Botão 'Exportar' clicado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao clicar no botão 'Exportar': {e}")

        # Passo 2: Preenche as datas
        try:
            # Preenche data de início
            page.click("input[type='date']")
            page.fill("input[type='date']", data_inicio)
            st.success(f"✅ Data de início preenchida: {data_inicio}")

            # Preenche data de fim
            page.click("input[type='date']")
            page.fill("input[type='date']", data_fim)
            st.success(f"✅ Data de fim preenchida: {data_fim}")
        except Exception as e:
            st.error(f"❌ Erro ao preencher as datas: {e}")

        # Passo 3: Clicar no botão "Gerar Relatório"
        try:
            gerar_relatorio = page.query_selector("button[type='submit']")
            gerar_relatorio.click()
            st.success("✅ Botão 'Gerar Relatório' clicado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao clicar no botão 'Gerar Relatório': {e}")

        # Aguarda o download do arquivo (opcional)
        page.wait_for_timeout(5000)  # Espera 5 segundos para download

        # Fecha o navegador
        browser.close()

# Interface do Streamlit
st.title('Automação de Exportação de Relatório')

# Criação dos widgets de data
data_inicio = st.date_input("Selecione a data de início", datetime(2023, 1, 1))
data_fim = st.date_input("Selecione a data de fim", datetime.now())

# Botão para iniciar a automação
if st.button('Gerar Relatório'):
    data_inicio_str = data_inicio.strftime("%d/%m/%Y")
    data_fim_str = data_fim.strftime("%d/%m/%Y")
    
    st.write(f"Executando automação com as datas selecionadas: {data_inicio_str} a {data_fim_str}")
    
    # Chama a função para rodar a automação
    executar_automacao(data_inicio_str, data_fim_str)
