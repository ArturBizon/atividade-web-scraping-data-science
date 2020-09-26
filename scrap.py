# -*- encoding: utf-8 -*-
import time 
import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "http://apps.tre-sc.jus.br/site/fileadmin/arquivos/eleicoes/estatistica_eleitoral/estat_offline/perfil.htm"

attributes = {"Situacao": "50",
             "FaixaEtaria": "51",
             "GrauDeInstrucao": "52",
             "Genero":"53",
             "EstadoCivil": "54",}

def extract_table_data(table, fileName):
    linhas = table.find_elements_by_tag_name("tr")
    # Monta dict
    dic = {}
    dados = []

    for indice, coluna in enumerate(linhas[0].find_elements_by_tag_name("th")):
        outerhtml = coluna.get_attribute('outerHTML')
        tag_value = re.search(">(.+?)<",outerhtml).group(1)
        dados.append([tag_value.replace(".", "")])

    for linha in linhas[1:]:
        colunas = linha.find_elements_by_tag_name("td")
        for indice, coluna in enumerate(colunas):
            outerhtml = coluna.get_attribute('outerHTML')
            tag_value = re.search(">(.+?)<",outerhtml).group(1)
            dados[indice].append(tag_value.replace(".", ""))

    for indice, coluna in enumerate(dados):
        dic[coluna[0]] = coluna[1:]

    df = pd.DataFrame(dic)
    df.to_csv(fileName,index=False,encoding="latin_1")
    pass


driver = webdriver.Chrome(r"C:\Users\abizon\Documents\IntroducaoDataScience\AtividadeWebScrapping\chromedriver.exe")  # Optional argument, if not specified will search path.
driver.get(url);
for key in attributes:
    # time.sleep(1) # Let the user actually see something!
    select = driver.find_element_by_name('lstCategoria')
    allOptions = select.find_elements_by_tag_name("option")
    for option in allOptions:
        if option.get_attribute("value") == attributes[key]:
            option.click()
    # time.sleep(1) # Let the user actually see something!

    btnSearch = driver.find_element_by_name("GO")
    btnSearch.click()
    # time.sleep(1)
    tabela = driver.find_element_by_css_selector('table.appDataTable')

    extract_table_data(tabela, key+".csv")
    time.sleep(1)
    driver.back()
driver.quit()