import pandas as pd
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configurações do Chrome

# Caminho para o diretório de perfil do Chrome
userdir = 'c:\\chromewithlogin'

# Configurar opções do Chrome
options = Options()
options.add_argument(f"--user-data-dir={userdir}")

# Cria o driver
driver = webdriver.Chrome(options=options)

# URL do site da amazon
url = 'https://logistics.amazon.com.br/account-management/delivery-associates?providerType=DA&providerStatus=ONBOARDING&searchStart=0&searchSize=100'

# Acessa a página
driver.get(url)  

# Aguarda o carregamento da página
wait = WebDriverWait(driver, 10)

# Clica na div que abre o dropdown
dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "af-select__container__label")))
dropdown.click()

# Aguarda o item "Integração" estar presente no DOM
integracao = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'af-option') and normalize-space()='Integração']")))

# Usa JavaScript para forçar o clique
driver.execute_script("arguments[0].click();", integracao)

# Aguarda o carregamento da tabela
pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'af-button primary  af-search__search-button desktop') and normalize-space()='Pesquisar']"))) 

# Usa JavaScript para forçar o clique
driver.execute_script("arguments[0].click();", pesquisar)

# Aguarda o carregamento da pesquisa
time.sleep(3)

nomes_links = driver.find_elements(By.XPATH, "//table[contains(@class, 'af-table')]//a[@class='af-link']")
# Loop para abrir cada link em uma nova aba
for link in nomes_links:
    nome = link.text
    motorista = link.get_attribute("href")
    
    # Abrir em nova aba
    driver.execute_script("window.open(arguments[0]);", motorista)
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(5)  # Aguarda a aba carregar

    # Aguarda o carregamento da div onbording
    botao_onboarding = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.af-expander__heading")))

    # Clica via JavaScript
    driver.execute_script("arguments[0].click();", botao_onboarding)

    # Faz a verificação da carteira de motorista
    carteira_motorista = driver.find_element(By.CLASS_NAME, "onboarding-task-header")

    # Busca a tag <i> dentro da div
    icon = carteira_motorista.find_element(By.TAG_NAME, "i")

    # Verifica as classes da tag <i>
    classes = icon.get_attribute("class")

    if "fa-minus" in classes:
        print("certo")  
    elif "fa-check" in classes:
        print("errado")
    else:
        print("classe não reconhecida")

    # Espera para visualização do clique
    time.sleep(2)

    driver.close()  # Fecha a aba atual
    driver.switch_to.window(driver.window_handles[0])  # Retorna para a aba principal


