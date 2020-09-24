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

driver = webdriver.Chrome(r"C:\Users\abizon\Documents\IntroducaoDataScience\AtividadeWebScrapping\chromedriver.exe")  # Optional argument, if not specified will search path.
driver.get(url);
time.sleep(1) # Let the user actually see something!
select = driver.find_element_by_name('lstCategoria')
allOptions = select.find_elements_by_tag_name("option")
for option in allOptions:
    if option.get_attribute("value") == '52':
       option.click()
time.sleep(1) # Let the user actually see something!

btnSearch = driver.find_element_by_name("GO")
btnSearch.click()
time.sleep(1)
tabela = driver.find_element_by_css_selector('table.appDataTable')
linhas = tabela.find_elements_by_tag_name("tr")
#pesquise pelo Irani
for linha in linhas[1:]:
    colunas = linha.find_elements_by_tag_name("td")
    outerhtml = colunas[0].get_attribute('outerHTML')
    tag_value = re.search(">(.+?)<",outerhtml).group(1)
    #print(tag_value)
    if tag_value == "IRANI":
        print(linha.get_attribute('outerHTML'))
    

time.sleep(5)
driver.quit()

