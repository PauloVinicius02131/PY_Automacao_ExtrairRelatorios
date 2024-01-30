# Bibliotecas
from multiprocessing.connection import wait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from datetime import timedelta
import os
import sys

# Encontrar caminho do chrome driver
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# Variavel do driver
path = application_path + '\chromedriver'
driver = webdriver.Chrome(path)
driver.maximize_window()

driver.get("http://sistema.sstelematica.com.br/")


def funcaoLogin():
    try:
        # Email
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'formUsrLogin'))).send_keys('@gmail.com')

        # Senha
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'formPasswordLogin'))).send_keys("zzzzz")

        # Achar Botão Login
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'enter'))).click()

    except:
        print('Erro no Login')
        input('Pressione Enter para continuar...')
        driver.quit()


def funcaoSkipTour():
    try:
        # Botão Agora Não
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/button"))).click()
    except:
        print('TimeOut na SkipTour')
        input('Pressione Enter para tentar novamente.')
        funcaoSkipTour()


def abrirRelatorio():
    try:
        # Abrir DropDown Relatórios.
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'relatorios'))).click()

        # Abrir Relatório Histórico Completo.
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID,
                                        "#widgets/reportcomplete/reportcomplete.html"))).click()

        WebDriverWait(driver, 30).until(
            EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[6]")))

        print('Relatório Aberto')
    except:
        print('Erro no Abrir Relatorios')
        input('Pressione Enter para tentar novamente.')
        abrirRelatorio()


def filtrosRelatoriosCompleto():
    # Variáveis do filtro de data.
    data_fim = date.today()
    data_inicio = date.today() - timedelta(days=1)

    # Preencher campo data inicio.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'start_day')))
    driver.find_element(By.ID, 'start_day').clear()
    driver.find_element(By.ID, 'start_day').send_keys(
        data_inicio.strftime("%d/%m/%Y"))

    # Preencher campo data fim.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'end_day')))
    driver.find_element(By.ID, 'end_day').clear()
    driver.find_element(By.ID, 'end_day').send_keys(
        data_fim.strftime("%d/%m/%Y"))

    # Selecionar todos os tipos de transmissões.
    driver.find_element(By.XPATH,
                        "/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[1]/div[2]/div[3]/div/ul/li/a").click()

    # Colunas Adicionais
    driver.find_element(By.XPATH, '//*[@id="ui-accordion-1-header-0"]').click()
    # Selecionar todas as colunas adicionais
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[2]/div/div[1]/div/div[1]/a/i"))).click()

    # Todas as empresas
    elementos = Select(driver.find_element(By.ID, 'subgroup'))
    element = len(elementos.options)
    for items in range(element):
        elementos.select_by_index(items)

    # Agora devo confeccionar uma lista com todos os veículos da unidade para que seja gerado um relatório para cada um.

    # Aguardar resultado filtro empresa.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[3]/div/div[4]/select/option[2]')))

    # Lista dos veículos
    grupoveiculos = Select(driver.find_element(By.ID, 'unit'))
    veiculos = range(len(grupoveiculos.options))
    veiculos = [i for i in veiculos if i != 0]

    grupoveiculos.deselect_all()

    for item in veiculos:
        # Selecionar Veiculo do range no Dropbox.
        grupoveiculos.select_by_index(item)

        testegerar = 1

        while testegerar == 1:
            # Botão Gerar Relatório.
            driver.find_element(By.XPATH,
                                '/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[6]/button').click()

            # Aguarde aba do relatório aberta.
            WebDriverWait(driver, 300).until(
                EC.invisibility_of_element((By.CLASS_NAME, "spinner-small")))

            print('Término Carregamento 1')

            try:
                WebDriverWait(driver, 300).until(
                    EC.invisibility_of_element((By.CLASS_NAME, "spinner-small")))

                driver.find_element(By.CLASS_NAME, 'alert')
                print('Achei Erro')

                WebDriverWait(driver, 300).until(
                    EC.invisibility_of_element((By.CLASS_NAME, "alert")))

            except:
                print('Não Achei Erro')
                testegerar = 0

        # Esperar todas as linhas do relatório serem geradas.
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script("return jQuery.active == 0"))

        # Expandir Ações.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdown-toggle")))

        driver.find_element(By.CLASS_NAME,
                            'dropdown-toggle').click()

        # Por ser um elemento javascript é necessário o document.
        # Poderia declarar como variavel o conteúdo dentro do parenteses.
        driver.execute_script(
            "document.getElementsByClassName('a_csv')[0].click()")

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "panel-loader")))

        imagemfechar = driver.find_element(By.CLASS_NAME,
                                           "closeReportTab")
        driver.execute_script("arguments[0].click();", imagemfechar)

        grupoveiculos.deselect_all()

        driver.find_element(
            By.XPATH, "/html/body/div[3]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/form/div[3]/div/div[5]/div[2]/div/a").click()

        # time.sleep(5)
