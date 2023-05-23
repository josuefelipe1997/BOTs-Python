import time
import os
import os.path
import pyautogui
import datetime
import logging
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
logging.basicConfig(level= logging.INFO, filename=r'./Digitos_Higienizados.log')

while True:
    try:
        num_arquivos = int(input("\nNumero arquivos que deseja higienizar: "))
        if num_arquivos > 0:
            num_arquivos +=1
            break
        elif num_arquivos <= 0:
            print('\nValor invalido, tente novamente\n')
    except:
        print('\nValor invalido, tente novamente\n')
        
while True:
    try:
        digito = int(input("\nInforme o digito que deseja iniciar a higienização: "))
        if digito > 0:
            break
        elif digito <= 0:
            print('\nValor invalido, tente novamente\n')
    except:
        print('\nValor invalido, tente novamente\n')
        
while True:
    try:
        count = int(input("\nInforme o numero da planilha que deseja iniciar a higienização: "))
        if count >= 0:
            break
        elif count < 0:
            print('\nValor invalido, tente novamente\n')
    except:
        print('\nValor invalido, tente novamente\n')
        
url = 'https://sistemavanguard.com.br/vanguard/index.php/'
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-session-crashed-bubble")
options.add_argument("--disable-popup-blocking")
options.add_argument("--incognito")    
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', chrome_options=options)
driver.maximize_window()
driver.get(url)

user = driver.find_element(By.XPATH, '//*[@id="exten"]').send_keys('USUARIO')
pas = driver.find_element(By.XPATH,'//*[@id="login-form"]/div[3]/div/input').send_keys('SENHA')
login = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)

driver.get('https://sistemavanguard.com.br/vanguard/index.php/solicitarlote2')
time.sleep(2)

while True:
    
    data = datetime.datetime.now()
    data_formatada = (str(data.day) + "/" + "0" + str(data.month) + "/" + str(data.year) + ' ' + str(data.hour) + ":" + str(data.minute) + ":" + str(data.second))    
    hora_atual = (str(data.hour))
    hora_atual = (int(hora_atual)) 
            
    if(hora_atual > 20):
        break
    
    while True:
        try:
            for campanha in range(1,16):
                time.sleep(2)
                driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[10]/a[2]/i').click()
                time.sleep(2)
                diretorio = os.getcwd() + f"\Digitos\Digito_{digito}\{count}.csv"
                driver.find_element(By.XPATH, '//*[@id="perfilInss"]/div[2]/input').send_keys(diretorio)
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="formulario"]/div[1]/div[4]/button').click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="inputCheck"]').click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="inputEnviar"]').click()
                time.sleep(2)
                driver.get('https://sistemavanguard.com.br/vanguard/index.php/solicitarlote2')
                count +=1
            break
        except:
            time.sleep(1)
            driver.get('https://sistemavanguard.com.br/vanguard/index.php/solicitarlote2')
            time.sleep(2)
 
    finalizado = os.getcwd() + "\Finalizada.PNG"

    while True:
        for i in range(4):
            pyautogui.press('down')
        time.sleep(1)
        if pyautogui.locateCenterOnScreen(finalizado):   
            break
        else:
            time.sleep(30)
            driver.get('https://sistemavanguard.com.br/vanguard/index.php/solicitarlote2')
            time.sleep(2)
   
    for campanha in range(1,16):
        while True:
            try:
                driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/table/tbody/tr[{campanha}]/td[10]/a[4]/i').click()
                time.sleep(2)
                agencia = Select(driver.find_element_by_id('agencia'))
                time.sleep(1)
                agencia.select_by_value('5433')
                time.sleep(3)
                lote = Select(driver.find_element_by_id('lote'))
                time.sleep(1)
                lote.select_by_value('AGILUS 2019')
                time.sleep(1.5)
                driver.find_element(By.XPATH, '//*[@id="formulario"]/div[2]/div[8]/button').click()
                time.sleep(5)
                break
            except:
                pass
        while True:
            try:
                driver.find_element(By.XPATH, '//*[@id="md-ipbox"]/div/div/div[3]/button').click()
                break         
            except:
                pass
        time.sleep(1)
                           
    logging.info(f"{data_formatada} Foi Higienizado 750.000 cpf's do digito {digito} - Usuário FLIX")

    if count >= (num_arquivos - 1):
        if digito <= 10:
            digito += 1
            count = 0
        else:
            break