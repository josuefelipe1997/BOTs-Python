import time
import pandas as pd
import os.path
import datetime
import pywhatkit as kt
import pyautogui
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from logging import error
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

url = 'http://187.115.207.139:8000/calls?page=3'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options
driver.get(url)
user = driver.find_element_by_name('username')
user.send_keys('USUARIO')
pas = driver.find_element_by_name('password')
pas.send_keys('SENHA')
login = driver.find_element_by_name('commit').click()
time.sleep(0.5)

while True:
    clearConsole()
    count_atentida = 0
    count_responde = 0
    count_area = 0
    count_canal = 0
    count_discando = 0
    aux = 0
    
    try:  
        driver.get(url)
        df_status = pd.read_html(driver.find_element_by_id("index_wrapper").get_attribute('outerHTML'))[0]
           
        for i in range(len(df_status['Status'])):          
            if(i >= 1):
                aux = i-1      
            if(df_status['Status'][i] == df_status['Status'][aux] and df_status['Status'][i] == 'Não atendida'):
                count_atentida +=1
                if count_atentida >= 20:
                    verificador_status = df_status['Status'][i]            
            elif(df_status['Status'][i] == df_status['Status'][aux] and df_status['Status'][i] == 'Não Responde'):
                count_responde += 1
                if count_responde >= 20:
                    verificador_status = df_status['Status'][i]       
            elif(df_status['Status'][i] == df_status['Status'][aux] and df_status['Status'][i] == 'Fora de Área'):
                count_area += 1
                if count_area >= 20:
                    verificador_status = df_status['Status'][i]            
            elif(df_status['Status'][i] == df_status['Status'][aux] and df_status['Status'][i] == 'Sem Canal Disponível'):
                count_canal += 1
                if count_canal >= 20:
                    verificador_status = df_status['Status'][i]
                                           
        print(f'Chamadas Não Atendidas: {count_atentida}')
        print(f'Chamadas Não Responde: {count_responde}')
        print(f'Chamada Fora de Área: {count_area}')
        print(f'Chamada Sem Canal Disponível: {count_canal}')
        
        if count_atentida >= 0 or count_responde >= 0 or count_area >= 0 or count_canal >= 0:
            data = datetime.datetime.now()
            hora = str(data.hour) + ':' + str(data.minute) + ':' + str(data.second)
            kt.sendwhatmsg_instantly("+5531973387903", 'SYSTEM INFORMATION: Mais de 10 {verificador_status} seguidos as {hora}')
            time.sleep(5)
            while True:
                try:
                    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[3]').click()
                    break
                except:
                    continue  
            pyautogui.press('enter')            
    except Exception as e:
        print('Erro :')
        print ('Tipo: ', type(e)) 
        print ('Argumentos: ', e.args)
        print (e)  
        print("Tente novamente !!!")
  
    time.sleep(2)