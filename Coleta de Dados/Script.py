from operator import itemgetter
import time
import pandas as pd
import os
import os.path
from pandas.io.parsers import read_csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from tokenize import Ignore
from random import *
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

url = 'https://sistemavanguard.com.br/vanguard/index.php/'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver')#, options=options
driver.get(url)

user = driver.find_element(By.XPATH, '//*[@id="exten"]').send_keys('USUARIO')
pas = driver.find_element(By.XPATH,'//*[@id="login-form"]/div[3]/div/input').send_keys('SENHA')
login = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()
time.sleep(2)

driver.get('https://sistemavanguard.com.br/vanguard/index.php/listacampanha')
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[4]/div[1]/a').click()

df = pd.read_html(driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/div/div/table").get_attribute('outerHTML'))[0]

for indice, campanha in enumerate(df['Nome']):
    if campanha == '5433 - INSS - PERFIL DE CLIENTES':
        valor = indice + 1 
            
time.sleep(2)       
driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{valor}]/td[2]/a').click()
time.sleep(2)

colunas = ['NB', 'Nome', 'CPF', 'Nascimento', 'Bloqueio', 'DIB', 'DDB', 'Especie','Meio Pagamento', 'Banco', 'Ag. Banco',
           'Conta Corrente', 'Endereco', 'CEP', 'Bairro', 'Cidade - UF',
           'Cel. 1', 'Cel. 2', 'Cel. 3', 'Fixo 1', 'Fixo 2',
           'MR','Base de Calculo','Margem 35%','Margem Disponivel Cartão']

df_final = pd.DataFrame(columns=colunas)
count = 0
refresh = 0

while True:
    
    timer_1 = randint(3,7)
    timer_2 = randint(2,6)
    timer_3 = randint(3,4)
    
    try:
        time.sleep(timer_1)
        
        try:
            driver.find_element_by_xpath('//*[@id="listaBeneficios"]/div/div/a').click()
        except Exception:
            pass
        
        time.sleep(timer_2) 
        driver.find_element(By.XPATH, f'//*[@id="btnOcultar"]').click()
        time.sleep(timer_3)
        
        df_esqueda = pd.read_html(driver.find_element_by_xpath('//*[@id="content-dados-cliente"]/div[1]/div[1]/div/div[2]/div/div[1]/table').get_attribute('outerHTML'))[0]
        df_direita = pd.read_html(driver.find_element_by_xpath('//*[@id="content-dados-cliente"]/div[1]/div[1]/div/div[2]/div/div[2]/table').get_attribute('outerHTML'))[0]
        df_telefone = pd.read_html(driver.find_element_by_xpath('//*[@id="telefonesHot"]/div/div[2]').get_attribute('outerHTML'))[0]
        df = pd.DataFrame(columns=colunas)
            
        for index,item in enumerate(df_esqueda[1]):
            lista = []
            lista.append(item)
            df[colunas[index]] = lista
                    
        for induce, item in enumerate(df_direita[1]):
            lista = []
            lista.append(item)
            index += 1
            df[colunas[index]] = lista
                
        for item in df_telefone.columns[1]:
            lista = []
            lista.append(item)
            index += 1       
            df[colunas[index]] = lista
            
        for item in range(0,5):
            if item !=0:
                limites = driver.find_element(By.XPATH, f'//*[@id="content-dados-cliente"]/div[2]/div[{item}]/div/div[2]').text
                lista = []
                lista.append(limites)  
                df[colunas[index]] = lista
                index += 1 
                
        df_final.loc[len(df_final)] = df.loc[0]
        df_final = df_final.replace({'Unnamed: 1_level_1':'0', 'Unnamed: 1_level_2':'0','Unnamed: 1_level_3':'0','Unnamed: 1_level_4':'0'}, regex=True)
        df_final = df_final[['NB', 'Nome', 'CPF', 'Nascimento', 'Bloqueio', 'DIB', 'DDB', 'Especie','Meio Pagamento', 'Banco', 'Ag. Banco',
           'Conta Corrente', 'Endereco', 'CEP', 'Bairro', 'Cidade - UF',
           'MR','Base de Calculo','Margem 35%','Margem Disponivel Cartão',
           'Cel. 1', 'Cel. 2', 'Cel. 3', 'Fixo 1', 'Fixo 2']]  
        df_final.to_csv((f'Base_Vanguard.csv'), sep=';', index=False)
        count +=1   
            
        clearConsole()
        
        print(f'Cliente coletados: {count}') 
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/form/div[2]/a').click()      
    except Exception:
        refresh+=1        
        if refresh >= 5 and refresh <= 10:
            driver.refresh()
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[@id="listaBeneficios"]/div/div/a').click() 
            except:
                continue
        elif refresh > 10:
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/form/div[2]/a').click()
            refresh = 0
        continue