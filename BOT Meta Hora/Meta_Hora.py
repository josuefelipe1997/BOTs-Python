import time
import pandas as pd
import os
import os.path
import datetime
from pandas.io.parsers import read_csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from logging import error
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def API():
    
    if(hora_atual <= 14):
        SAMPLE_SPREADSHEET_ID = '18540RMAHqXMRrtYCpe1Ot49zCxatThBagHdbyuxIWh4' #Planilha Manhã
    elif(hora_atual >= 15):
        SAMPLE_SPREADSHEET_ID = '1vrHaxcgVn2387ql7BqmhzsRkaB5IBIx6_3HKmCOdXCY' #Planilha Tarde
    
    creds = None   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=f"{celula}!A1:Z").execute()
    values = result.get('values', [])
    
    count_vazio = 0
    count_cheio = 0
    
    for item in values:
        if (len(item) == 0):
            count_vazio +=1
    
    for item in values:
        if (len(item) != 0):
            count_cheio +=1
        else:
            linha = count_cheio
               
    if(count_vez < 1):
        ultima_linha = len(values) + 2     
    elif(count_vez >= 1):           
        ultima_linha = linha + count_vazio  + 1  
         
    SAMPLE_RANGE_NAME = f"{celula}!A{ultima_linha}"
    
    importa = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                   range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", 
                                   body={"values":listas}).execute()

count_vez = 0

while True:
    
    url = 'http://187.115.207.139:8000/login/signin' 
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options
    driver.get(url)
    user = driver.find_element_by_name('username')
    user.send_keys('bot.flix')
    pas = driver.find_element_by_name('password')
    pas.send_keys('flix.2021')
    login = driver.find_element_by_name('commit').click()
    time.sleep(0.5)
    
    clearConsole()
    
    data = datetime.datetime.now()
    data_formatada = (str(data.day) + "/" + "0" + str(data.month) + "/" + str(data.year))    
    hora_atual = (str(data.hour))
    hora_atual = (int(hora_atual))
    
    if (hora_atual <= 14 ):
        hora = "07:00:00"
    elif(hora_atual >= 15):
        hora = "14:00:00"

    try:
        url_chamadas = 'http://187.115.207.139:8000/calls?interval%5Bselect%5D=custom&interval%5Bstart_date%5D=10%2F12%2F2021&interval%5Bstart_time%5D=00%3A00%3A00&interval%5Bend_date%5D=10%2F12%2F2021&interval%5Bend_time%5D=23%3A59%3A59&terminal=&agent=&queue%5Bdirection%5D=ALL&sort=&to_excel=0&to_csv=0&x=12&y=14&locality=&call_type_id=&carrier_id=&trunking_id=&directions%5B%5D=IN&directions%5B%5D=OUT&directions%5B%5D=AUTO&waits=Igual&call_waiting=&duration=Maior&duration_call=59&status%5Bselect%5D=&substatus%5Bselect%5D='
        driver.get(url_chamadas)
        time.sleep(0.5)
        
        driver.find_element_by_id('search-icon').click()
        time.sleep(0.5)
        
        driver.find_element_by_xpath('//*[@id="interval_start_date"]').clear()
        time.sleep(0.5) 
        driver.find_element_by_xpath('//*[@id="interval_start_date"]').send_keys(data_formatada)
        time.sleep(0.5)
        
        driver.find_element_by_xpath('//*[@id="interval_start_time"]').clear()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="interval_start_time"]').send_keys(hora)
        time.sleep(0.5)
        
        driver.find_element_by_xpath('//*[@id="interval_end_date"]').clear()
        time.sleep(0.5)  
        driver.find_element_by_xpath('//*[@id="interval_end_date"]').send_keys(data_formatada)
        time.sleep(0.5)
      
        driver.find_element_by_id('search-icon').click()  
        time.sleep(2)
        
        download = driver.find_elements_by_link_text('CSV')[0].click()
        time.sleep(2)

        caminho_arquivo = r'C:\Users\Josué\Downloads'
        nome = 'chamadas'

        for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
            for arquivo in arquivos:
                if nome in arquivo:
                    caminho_completo = os.path.join(raiz, arquivo)
                    nome_arquivo, ext_arquivo = os.path.splitext(arquivo)
                    chamadas = (caminho_completo)
                                                    
        df_tabela_chamadas = pd.read_csv(chamadas, encoding='UTF-8', sep=';')
        os.remove(chamadas) 
              
        df_tabela_chamadas['Tipo'] = df_tabela_chamadas['Tipo'].replace('á','a', regex=True)
        df_tabela_chamadas.rename(columns={'Data':'', 'Tipo':'','Numero':'', 'Agente':'', 'Fila':'', 'Duracao':'', 'Espera':'', 'Posicao':'', 'Oferecimentos':'', 'Status':''}, inplace=True)
        df_tabela_chamadas.fillna(0, inplace=True)
        listas = df_tabela_chamadas.values.tolist()
        celula = "Chamadas"
        
        API()  
        count_vez += 1
        driver.quit()
        
        print(f'\n\nMETA HORA DE {hora_atual}H ATUALIZADA COM SUCESSO!!!')
        time.sleep(3600)
        
    except Exception as e:
        print('Erro :')
        print ('Tipo: ', type(e)) 
        print ('Argumentos: ', e.args)
        print (e)
        print("Tente novamente !!!")  
    
    if(hora_atual > 20):
        break
    
driver.quit()