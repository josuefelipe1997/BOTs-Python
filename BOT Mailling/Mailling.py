import time
import pandas as pd
import datetime
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

url_vonix = 'http://187.115.207.139:8000/admin/dialer'
url_vanguard = 'https://sistemavanguard.app/vanguard/index.php/solicitarlote2'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options

usuario_tristerix = input('Usuário Tristerix: ')
senha_tristerix = getpass.getpass('\nSenha Tristerix: ')

usuario_vanguard = input('Usuário Vanguard: ')
senha_vanguard = getpass.getpass('\nSenha Vanguard: ')

def seleciona_fila(cod_fila):
    sel = Select(driver.find_element_by_id('agencia'))
    sel.select_by_value("5433")
    time.sleep(0.5)
    sel = Select(driver.find_element_by_id('tipo_telefone'))
    sel.select_by_value("T")
    time.sleep(0.5)
    sel = Select(driver.find_element_by_id('apagar'))
    sel.select_by_value("Y")
    time.sleep(0.5)
    driver.find_element(By.XPATH, cod_fila).click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="formulario"]/div[2]/div[6]/button').click()
    
while True:
    filas_vazias = []  
    driver.get(url_vonix)
    time.sleep(2)
    try:
        driver.find_element(By.NAME, 'username').send_keys(usuario_tristerix)
        driver.find_element(By.NAME, 'password').send_keys(senha_tristerix)
        driver.find_element(By.NAME, 'commit').click()
        time.sleep(2)
    except:
        continue
    
    while True:       
        try:   
            df_filas_tristerix = pd.read_html(driver.find_element_by_id("active_table").get_attribute('outerHTML'))[0]
            df_filas_tristerix = df_filas_tristerix.sort_values(by=['Fila'])
            for indice, linha in df_filas_tristerix.iterrows():
                if linha['Status'] == 'Sem contatos':
                    filas_vazias.append(linha['Fila'])                     
            if len(filas_vazias) > 0:
                break
            else:
                driver.get(url_vonix)
                time.sleep(30)
        except:
            continue
    
    data = datetime.datetime.now() 
    hora_atual = (str(data.hour))
    hora_atual = (int(hora_atual))
    if(hora_atual >= 20):
        print(f'{hora_atual}H sistema encerrado !!!')
        break
        
    driver.get(url_vanguard)
    time.sleep(2)   
    try:
        driver.find_element(By.XPATH, '//*[@id="exten"]').send_keys(usuario_vanguard)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/div/input').send_keys(senha_vanguard)
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
        time.sleep(1)
    except:
        continue

    driver.get(url_vanguard)
    time.sleep(1)
    
    for fila in filas_vazias:   
        if fila == 'FLIX FILA 01 - [14250]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[10]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue                        
        elif fila == 'FLIX FILA 02 - [17092]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[2]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[22]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue     
        elif fila == 'FLIX FILA 03 - [17093]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[3]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[23]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue                        
        elif fila == 'FLIX FILA 04 - [17094]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[4]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[24]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue           
        elif fila == 'FLIX FILA 05 - [17887]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[5]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[25]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue           
        elif fila == 'FLIX FILA 06 - [26037]':
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[6]/td[10]/a[4]/i').click()
                    time.sleep(1)
                    seleciona_fila('//*[@id="lote2"]/option[51]')
                    driver.get(url_vanguard)
                    time.sleep(1)
                    break
                except:
                    continue