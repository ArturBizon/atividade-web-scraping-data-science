# -*- encoding: utf-8 -*-

#Alunos: Artur Bizon e Gianluca Scheidemantel

import time 
import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "http://apps.tre-sc.jus.br/site/fileadmin/arquivos/eleicoes/estatistica_eleitoral/estat_offline/perfil.htm"
driverPath = r"C:\Users\abizon\Documents\IntroducaoDataScience\AtividadeWebScrapping\chromedriver.exe"
attributes = {"Situacao": "50",
             "FaixaEtaria": "51",
             "GrauDeInstrucao": "52",
             "Genero":"53",
             "EstadoCivil": "54",}

def extract_table_data(table, fileName):
    rows = table.find_elements_by_tag_name("tr")
    # Monta dict
    dic = {}
    data = []

    #Carrega cabecalho
    for index, column in enumerate(rows[0].find_elements_by_tag_name("th")):
        outerhtml = column.get_attribute('outerHTML')
        tag_value = re.search(">(.+?)<",outerhtml).group(1)
        data.append([tag_value.replace(".", "")])
        
    #Carrega os dados
    for row in rows[1:]:
        columns = row.find_elements_by_tag_name("td")
        for index, column in enumerate(columns):
            outerhtml = column.get_attribute('outerHTML')
            tag_value = re.search(">(.+?)<",outerhtml).group(1)
            data[index].append(tag_value.replace(".", ""))

    # Transforma a matriz em dicionario para gerar o dataGrame
    for index, column in enumerate(data):
        dic[column[0]] = column[1:]

    df = pd.DataFrame(dic)
    df.to_csv(fileName, index=False, encoding="latin_1")
    pass


driver = webdriver.Chrome(driverPath)
driver.get(url)

for key in attributes:
    # time.sleep(1) 
    select = driver.find_element_by_name('lstCategoria')
    allOptions = select.find_elements_by_tag_name("option")
    for option in allOptions:
        if option.get_attribute("value") == attributes[key]:
            option.click()
    # time.sleep(1) 

    btnSearch = driver.find_element_by_name("GO")
    btnSearch.click()
    # time.sleep(1)
    table = driver.find_element_by_css_selector('table.appDataTable')

    extract_table_data(table, key+".csv")
    # time.sleep(1)
    driver.back()
driver.quit()