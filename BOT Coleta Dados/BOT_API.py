import time
import pandas as pd
import datetime
import os
import getpass
import os.path
from logging import error
from pandas.io.parsers import read_csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']#Escopo que ira permitir o que o sistema podera fazer na planilha (editar ou apenas ler)
SAMPLE_SPREADSHEET_ID = '1zzONe7A6yk-ynzX7T7rF-6LIEM5wgYwX0Snh8Uh_DoY' #ID da minha planilha

def API():
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
    
    ultima_linha = len(values) + 1
    SAMPLE_RANGE_NAME = f"{celula}!A{ultima_linha}"
    
    importa = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                   range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", 
                                   body={"values":listas}).execute()
    

# Faz Login no Tristerix e pega a data atual
url = 'http://187.115.207.139:8000/login/signin'
data = datetime.datetime.now()
data_formatada = (str(data.day) + "/" + str(data.month) + "/" + str(data.year))
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options
driver.get(url)

while True:
    try:
        usuario = input('Usuário: ')
        senha = getpass.getpass('\nSenha: ')   
        driver.find_element(By.NAME, 'username').send_keys(usuario)
        driver.find_element(By.NAME, 'password').send_keys(senha)
        driver.find_element(By.NAME,'commit').click()
        time.sleep(0.5)
        break
    except:
        print('Usuário ou Senha Incorreto, Tente Novamente')

#################################################### CHAMADAS #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# URL que acessa a página "Chamadas" com as opções preenchidas
url_chamadas = 'http://187.115.207.139:8000/calls?interval%5Bselect%5D=today&interval%5Bstart_date%5D=06%2F01%2F2022&interval%5Bstart_time%5D=00%3A00%3A00&interval%5Bend_date%5D=06%2F01%2F2022&interval%5Bend_time%5D=23%3A59%3A59&terminal=&agent=&queue%5Bdirection%5D=ALL&sort=&to_excel=0&to_csv=0&x=20&y=21&locality=&call_type_id=&carrier_id=&trunking_id=&directions%5B%5D=IN&directions%5B%5D=OUT&directions%5B%5D=AUTO&waits=Igual&call_waiting=&duration=Maior&duration_call=10&status%5Bselect%5D=completed&substatus%5Bselect%5D='
driver.get(url_chamadas)
time.sleep(2)

att = driver.find_element_by_id('search-icon').click()
time.sleep(2)

# Baixa o arquivo .csv
download = driver.find_elements_by_link_text('CSV')[0].click()
time.sleep(5)

# Faz uma busca na pasta Downloads e acha o arquivo de acordo com o nome.
caminho_arquivo = r'C:\Users\Josué\Downloads'
nome = 'chamadas'

for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
    for arquivo in arquivos:
        if nome in arquivo:
            caminho_completo = os.path.join(raiz, arquivo)
            nome_arquivo, ext_arquivo = os.path.splitext(arquivo)
            chamadas = (caminho_completo)
        
# Abre o arquivo .csv coloca em um DataFrame e depois apaga o arquivo da pasta Download
df_tabela_chamadas = pd.read_csv(chamadas, encoding='UTF-8', sep=';')
os.remove(chamadas)

# Remove as colunas e salva o DataFrame em um arquivo .csv novamente
df_tabela_chamadas['Tipo'] = df_tabela_chamadas['Tipo'].replace('á','a', regex=True)
df_tabela_chamadas.rename(columns={'Data':'', 'Tipo':'','Numero':'', 'Agente':'', 'Fila':'', 'Duracao':'', 'Espera':'', 'Posicao':'',
                                   'Oferecimentos':'', 'Status':''}, inplace=True)

df_tabela_chamadas.fillna('', inplace=True)
listas = df_tabela_chamadas.values.tolist()
celula = "CHAMADAS"
API()

#################################################### AGENTES GERAL #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# URL que acessa a página "Agentes Geral"
url_geral = 'http://187.115.207.139:8000/agents/calls_overview?x=21&y=15&to_excel=0&interval%5Bselect%5D=today&interval%5Bstart_date%5D=06%2F01%2F2022&interval%5Bend_date%5D=06%2F01%2F2022'
driver.get(url_geral)
time.sleep(2)

att = driver.find_element_by_id('search-icon').click()
time.sleep(2)

# Pega os dados da Tabela "Online" e formata removendo informações inuteis
df_tabela_online = pd.read_html(driver.find_element_by_id("wrapper").get_attribute('outerHTML'))[0]
df_tabela_online['Agente'] = df_tabela_online['Agente'].replace('é','e', regex=True)
df_tabela_online['Tempo logado'] = df_tabela_online['Tempo logado'].replace({'h':'/', 'm':'/', 's':'', ' ':'','\(':'', '\)':''}, regex=True)
df_tabela_online['Índices'] = df_tabela_online['Índices'].replace({'h':'/', 'm':'/', 's':'', ' ':'','\(':'', '\)':''}, regex=True)


# Pega os dados da Tabela "Offline" e formata removendo informações inuteis
try:
    df_tabela_offline = pd.read_html(driver.find_element_by_id("wrapper").get_attribute('outerHTML'))[1]
    df_tabela_offline['Agente'] = df_tabela_offline['Agente'].replace('é','e', regex=True)
    df_tabela_offline['Tempo logado'] = df_tabela_offline['Tempo logado'].replace({'h':'/', 'm':'/', 's':'', ' ':'','\(':'', '\)':''}, regex=True)
    df_tabela_offline['Índices'] = df_tabela_offline['Índices'].replace({'h':'/', 'm':'/', 's':'', ' ':'','\(':'', '\)':''}, regex=True)


    # Concatena os dois DataFrames em um único
    df = pd.concat([df_tabela_online, df_tabela_offline], ignore_index=True)
except IndexError as erro:
    print('Tabela Offline não existe nesse momento')
    df = df_tabela_online

df = df.droplevel(level=0, axis=1)

df[['Horas','Minutos']] = df['TMO'].str.split('/', expand=True)
df[['Hora','Min','Sec']] = df['Tempo logado'].str.split('/', expand=True)
df = df.drop(columns=['Tempo logado', 'TMO'])

df.insert(loc=11, column='Segundos', value='', allow_duplicates=True)
df.insert(loc=14, column='Outras Filas',value='0,00%', allow_duplicates=True)
df.insert(loc=16, column='Data', value=data_formatada, allow_duplicates=True)

# Organiza as colunas do Dataframe na ordem desejada
df = df[['Agente', 'Hora', 'Min', 'Sec', 'Discadas', 'Automáticas', 'Recebidas', 'Rejeitadas', 'Atend./Hora','Horas','Minutos','Segundos','Chamadas', 'Discando','Outras Filas','Pausas', 'Ociosidade', 'Data']]

# Remove as colunas e salva o DataFrame em um arquivo
df.rename(columns={'Agente':'', 'Hora':'', 'Min':'', 'Sec:':'', 'Discadas':'', 'Automáticas':'', 'Recebidas':'', 'Rejeitadas':'','Atend./Hora':'','Horas':'','Minutos':'','Segundos':'','Chamadas':'', 'Discando':'','Pausas':'', 'Ociosidade':'', 'Data':''}, inplace=True)

df.fillna('', inplace=True)
listas = df.values.tolist()
celula = "GERAL"
API()

#################################################### AGENTES RANKING #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# URL que acessa a página "Agentes Ranking"
url_ranking = 'http://187.115.207.139:8000/agents/ranking?x=8&y=29&interval%5Bselect%5D=today&interval%5Bstart_date%5D=06%2F01%2F2022&interval%5Bstart_time%5D=00%3A00%3A00&interval%5Bend_date%5D=06%2F01%2F2022&interval%5Bend_time%5D=23%3A59%3A59'
driver.get(url_ranking)
time.sleep(2)

att = driver.find_element_by_id('search-icon').click()
time.sleep(2)

# Pega os dados da Tabela "Ranking" e formata removendo informações inuteis
df_tabela_ranking = pd.read_html(driver.find_element_by_id("maincontent").get_attribute('outerHTML'))[0]
df_tabela_ranking['Tempo Logado'] = df_tabela_ranking['Tempo Logado'].replace({'h':'/', 'm':'/', 's':'', ' ':''}, regex=True)
df_tabela_ranking['Tempo de Conversação'] = df_tabela_ranking['Tempo de Conversação'].replace({'h':'/', 'm':'/', 's':'', ' ':''}, regex=True)
df_tabela_ranking['Recebidas'] = df_tabela_ranking['Recebidas'].replace({'h':'/', 'm':'/', 's':'', ' ':''}, regex=True)

df_tabela_ranking[['Hora','Min','Sec']] = df_tabela_ranking['Tempo Logado']['Tempo Logado'].str.split('/', expand=True)
df_tabela_ranking[['Horas','Minutos','Segundos']] = df_tabela_ranking['Tempo de Conversação']['Total'].str.split('/', expand=True)
try:
    df_tabela_ranking[['H','M']] = df_tabela_ranking['Tempo de Conversação']['Média'].str.split('/', expand=True)
except Exception as e:
        df_tabela_ranking[['H']] = df_tabela_ranking['Tempo de Conversação']['Média'].str.split('/', expand=True)
        df_tabela_ranking.insert(loc=14, column='M', value='', allow_duplicates=True)

df_tabela_ranking.columns = df_tabela_ranking.columns.get_level_values(0) + '_' +  df_tabela_ranking.columns.get_level_values(1)

df_tabela_ranking = df_tabela_ranking.drop(columns=['Tempo Logado_Tempo Logado', 'Tempo de Conversação_Total', 'Tempo de Conversação_Média'])

df_tabela_ranking.rename(columns={'Agente_Agente':'Agente','Originadas_Total':'Total', 'Originadas_Únicas':'Únicas', 'Originadas_Completadas':'Completadas',
                                  'Originadas_Não Completadas':'Não Completadas','Recebidas_Atendidas':'Atendidas', 'Recebidas_Rejeitadas':'Rejeitadas', 'Hora_':'Hora',
                                  'Min_':'Min', 'Sec_':'Sec', 'Horas_':'Horas', 'Minutos_':'Minutos', 'Segundos_':'Segundos','H_':'H','M_':'M'}, inplace=True)

df_tabela_ranking = df_tabela_ranking[['Agente', 'Hora', 'Min', 'Sec', 'Total', 'Únicas', 'Completadas', 'Não Completadas', 'Atendidas','Rejeitadas','Horas','Minutos',
                                       'Segundos','H','M']]

df_tabela_ranking.insert(loc=15, column='S', value='', allow_duplicates=True)
df_tabela_ranking.insert(loc=16, column='Data', value=data_formatada, allow_duplicates=True)

df_tabela_ranking.fillna('', inplace=True)
listas = df_tabela_ranking.values.tolist()
celula = "RANKING"
API()

#################################################### AGENTES PAUSAS #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# URL que acessa a página "Agentes Pausas"
url_pausa = 'http://187.115.207.139:8000/agents/pauses?x=0&y=14&to_excel=0&interval%5Bselect%5D=today&interval%5Bstart_date%5D=06%2F01%2F2022&interval%5Bstart_time%5D=00%3A00%3A00&interval%5Bend_date%5D=06%2F01%2F2022&interval%5Bend_time%5D=23%3A59%3A59&report_types=analytical'
driver.get(url_pausa)
time.sleep(2)

att = driver.find_element_by_id('search-icon').click()
time.sleep(2)

# Pega os dados da Tabela "Agente Pausas"
df_tabela_pausas = pd.read_html(driver.find_element_by_id("pauses_wrapper").get_attribute('outerHTML'))[0]

# Modifica os caracteres especiais da coluna "Moivo da Pausa" por caracteres normais
df_tabela_pausas['Motivo da Pausa'] = df_tabela_pausas['Motivo da Pausa'].replace({'ç':'c', 'ã':'a', 'ê':'e'}, regex=True)

# Remove as colunas e salva o DataFrame em um arquivo .csv
df_tabela_pausas.rename(columns={'Agente':'', 'Motivo da Pausa':'', 'Início da Pausa':'', 'Fim da Pausa':''}, inplace=True)

df_tabela_pausas.fillna('', inplace=True)
listas = df_tabela_pausas.values.tolist()

celula = "PAUSAS"
API()

clearConsole()
fim = input('\n\nControle de produção atualizado, pressione ENTER para encerrar a aplicação !!!')

driver.quit()