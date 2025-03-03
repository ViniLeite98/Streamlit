import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Função que configura e executa o Selenium
def executar_automacao(data_inicio, data_fim):
    # Configuração do navegador em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Modo headless (sem interface gráfica)
    chrome_options.add_argument("--disable-gpu")  # Necessário para rodar headless no Linux
    chrome_options.add_argument("--no-sandbox")  # Necessário para o Chrome rodar em ambientes de container
    chrome_options.add_experimental_option("detach", True)  # Mantém o navegador aberto (se necessário)

    # Inicializa o WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Abre o site
    driver.get("https://portal.minhaagendaapp.com.br/agenda")
    wait = WebDriverWait(driver, 10)

    # Preenche login e senha
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys("viniciusleitesouza_1998@hotmail.com")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys("Hara@1998", Keys.RETURN)

    # Aguarda o carregamento da página após o login
    time.sleep(3)

    # Verifica se o menu "Agenda" está visível
    try:
        agenda_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Agenda')]"))).click()
        print("✅ Acessou a página Agenda")
    except Exception:
        pass

    # Aguarda o carregamento da página Agenda
    time.sleep(1)

    # Clica no botão "Exportar"
    try:
        botao_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeSmall.css-h2trc4-btnExport"))).click()
        print("✅ Botão 'Exportar' clicado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao clicar no botão 'Exportar': {e}")

    # Passo 1: Clica no campo "Todos profissionais"
    try:
        campo_profissionais = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=':rs:']"))).click()
        time.sleep(1)  # Aguarda o menu abrir
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Todos profissionais')]"))).click()
        print("✅ Selecionado 'Todos profissionais'")
    except Exception as e:
        print(f"❌ Erro ao selecionar 'Todos profissionais': {e}")

    # Preenche datas
    try:
        # Clica na data de início
        data_inicio_elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=':ru:']"))).click()
        time.sleep(1)  # Aguarda o seletor abrir
        data_inicio_elemento.send_keys(data_inicio)  # Preenche com a data de início
        data_inicio_elemento.send_keys(Keys.RETURN)  # Pressiona ENTER
        print(f"✅ Data de início preenchida: {data_inicio}")
    except Exception as e:
        print(f"❌ Erro ao preencher a data de início: {e}")

    # Clica na data de fim
    try:
        data_fim_elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=':r10:']"))).click()
        time.sleep(1)  # Aguarda o seletor abrir
        data_fim_elemento.send_keys(data_fim)  # Preenche com a data de fim
        data_fim_elemento.send_keys(Keys.RETURN)  # Pressiona ENTER
        print(f"✅ Data de fim preenchida: {data_fim}")
    except Exception as e:
        print(f"❌ Erro ao preencher a data de fim: {e}")

    # Passo 3: Clicar no botão "Gerar Relatório"
    try:
        gerar_relatorio_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div/button"))).click()
        print("✅ Botão 'Gerar Relatório' clicado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao clicar no botão 'Gerar Relatório': {e}")

    # Aguarda o download do arquivo (opcional)
    time.sleep(5)

    # Fecha o navegador
    driver.quit()

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
