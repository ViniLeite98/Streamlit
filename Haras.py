import streamlit as st
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import time

# Função que configura e executa a automação com Playwright (modo assíncrono)
async def executar_automacao(data_inicio, data_fim):
    async with async_playwright() as p:
        # Lança o navegador em modo headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Abre o site
        await page.goto("https://portal.minhaagendaapp.com.br/agenda")

        # Realiza login
        await page.fill("input[type='email']", "viniciusleitesouza_1998@hotmail.com")
        await page.fill("input[type='password']", "Hara@1998")
        await page.press("input[type='password']", "Enter")

        # Aguarda o carregamento da página após o login
        await page.wait_for_load_state("networkidle")

        # Acessa a página "Agenda"
        try:
            agenda_menu = await page.locator("//*[contains(text(), 'Agenda')]")
            await agenda_menu.click()
            print("✅ Acessou a página Agenda")
        except Exception:
            print("❌ Erro ao acessar a página Agenda")

        # Aguarda o carregamento da página Agenda
        time.sleep(1)

        # Clica no botão "Exportar"
        try:
            botao_exportar = await page.locator("button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeSmall.css-h2trc4-btnExport")
            await botao_exportar.scroll_into_view_if_needed()
            await botao_exportar.click()
            print("✅ Botão 'Exportar' clicado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao clicar no botão 'Exportar': {e}")

        # Passo 1: Clica no campo "Todos profissionais"
        try:
            campo_profissionais = await page.locator("//*[@id=':rs:']")
            await campo_profissionais.click()
            time.sleep(1)  # Aguarda o menu abrir
            await page.locator("//*[contains(text(), 'Todos profissionais')]").click()
            print("✅ Selecionado 'Todos profissionais'")
        except Exception as e:
            print(f"❌ Erro ao selecionar 'Todos profissionais': {e}")

        # Preenche datas
        try:
            # Clica na data de início
            data_inicio_elemento = await page.locator("//*[@id=':ru:']")
            await data_inicio_elemento.click()
            time.sleep(1)  # Aguarda o seletor abrir
            await data_inicio_elemento.fill(data_inicio)  # Preenche com a data de início
            await data_inicio_elemento.press("Enter")  # Pressiona ENTER
            print(f"✅ Data de início preenchida: {data_inicio}")
        except Exception as e:
            print(f"❌ Erro ao preencher a data de início: {e}")

        # Clica na data de fim
        try:
            data_fim_elemento = await page.locator("//*[@id=':r10:']")
            await data_fim_elemento.click()
            time.sleep(1)  # Aguarda o seletor abrir
            await data_fim_elemento.fill(data_fim)  # Preenche com a data de fim
            await data_fim_elemento.press("Enter")  # Pressiona ENTER
            print(f"✅ Data de fim preenchida: {data_fim}")
        except Exception as e:
            print(f"❌ Erro ao preencher a data de fim: {e}")

        # Passo 3: Clicar no botão "Gerar Relatório"
        try:
            gerar_relatorio_botao = await page.locator("/html/body/div[4]/div[3]/div/div[2]/div/button")
            await gerar_relatorio_botao.click()
            print("✅ Botão 'Gerar Relatório' clicado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao clicar no botão 'Gerar Relatório': {e}")

        # Aguarda o download do arquivo (opcional)
        time.sleep(5)

        # Fecha o navegador
        await browser.close()

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
    asyncio.run(executar_automacao(data_inicio_str, data_fim_str))
