import pyautogui
import os
import pandas as pd
import mysql.connector
import requests
import numpy as np
import logging
from mysql.connector import Error
from datetime import datetime
from tqdm import tqdm
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyautogui import click, moveTo
logging.basicConfig(level= logging.INFO, filename=r'./Erro_Automatico_DB.log')

# mostra o id do último grupo adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)
# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": msg}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e) 
token = '5780408120:AAHtrYs_0MjybWg7Nu_JDl207h3fgp4khMg'
chat_id = last_chat_id(token)

confimacao = r'.\Imagens\Confirmacao_Download.PNG'
reset = r'.\Imagens\Reset.PNG'

pyautogui.PAUSE = 2

data_dia = datetime.now()
data_registro = (str(data_dia.year) + '-' + str(data_dia.month) + '-' + str(data_dia.day))
data_formatada = (str(data_dia.day) + "/" + str(data_dia.month) + "/" + str(data_dia.year))
hora_bot = (str(data_dia.hour))
hora = (int(hora_bot)) - 1
dia = int(data_dia.day)
mes = int(data_dia.month)
ano = int(data_dia.year)

hora_atual = f'.\Imagens\Hora\{hora}.PNG'
hora_limite = f'.\Imagens\Hora\{(hora + 1)}.PNG'

url = 'https://maisvoip488.ipboxcloud.com.br:8944/ipbox/index.php#' 
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-session-crashed-bubble")
options.add_argument("--disable-popup-blocking")
options.add_argument("--incognito")    
driver = webdriver.Chrome(executable_path=r'.\bin\chromedriver.exe', chrome_options=options)
driver.maximize_window()
driver.get(url)
sleep(2)
pyautogui.click(1093, 803) # click tela
driver.find_element(By.XPATH,'//*[@id="login"]').send_keys('USUARIO')
driver.find_element(By.XPATH,'//*[@id="senha"]').send_keys('SENHA')
sleep(1)
driver.find_element(By.XPATH,'//*[@id="Login"]').click()
sleep(1)

########################################################################################### RQ4 ###########################################################################################

sleep(2)

driver.find_element(By.XPATH, '//*[@id="top5"]/a').click()
sleep(1)
driver.find_element(By.XPATH, '//*[@id="headmenu5"]/ul/li[2]/a/i').click()
sleep(1)
driver.find_element(By.XPATH, '//*[@id="lat118"]/a').click()
sleep(1)

pyautogui.click(445, 317) # Operacao
pyautogui.click(429, 349) # Selecionar Operacao
pyautogui.click(450, 471) # Data
pyautogui.click(432, 511) # Hoje
pyautogui.click(450, 471) # Data
pyautogui.click(448, 692) # Selecione
pyautogui.click(677, 761) # Seta Hora
pyautogui.click(679, 739) # Rola Barra Pra Baixo

while True:
    try:
        if pyautogui.locateCenterOnScreen(hora_atual):
            print('xesque')
            hora_selecionada = pyautogui.locateCenterOnScreen(hora_atual)
            moveTo(hora_selecionada)
            click()
            break
    except:
        pass

pyautogui.click(740, 759) # Seta Minuto
pyautogui.click(714, 463) # Minuto Inicial
pyautogui.click(957, 762) # Seta Hora limite

while True:
    try:
        if pyautogui.locateCenterOnScreen(hora_limite):
            hora_selecionada = pyautogui.locateCenterOnScreen(hora_limite)
            moveTo(hora_selecionada)
            click()
            break
    except:
        pass

pyautogui.click(1020, 760) # Seta Minuto Limite
pyautogui.click(1018, 688) # Barra Minuto Limite
pyautogui.scroll(500) # Rola barra pra cima
pyautogui.click(994, 448)  # Seleciona minuti limite
pyautogui.click(1077, 805) # Aplica Hora
pyautogui.click(592, 508) # Baixa CSV

while True:
    try:
        if pyautogui.locateCenterOnScreen(confimacao):
            fechar = pyautogui.locateCenterOnScreen(reset)
            moveTo(fechar)
            click()
            break 
    except:
        pass       
driver.switch_to.window(driver.window_handles[0])

try:
    caminho_arquivo = r'C:\Users\Administrator\Downloads'
    nome = 'aprovqual'
    for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
        for arquivo in arquivos:
            if nome in arquivo:
                caminho_completo = os.path.join(raiz, arquivo)
                rq4 = (caminho_completo)
    df_rq4 = pd.read_csv(rq4, encoding='UTF-8', sep=';')
    os.remove(rq4)
    df_rq4.rename(columns={'Telefone':'Tel'}, inplace=True)
    df_rq4[['Data','Hora']] = df_rq4['Data/Hora'].str.split(' ', expand=True)
    df_rq4['Tel'] = df_rq4['Tel'].str.replace('-', '.', n=1)
    df_rq4[['DDD','Telefone']] = df_rq4['Tel'].str.split('.', expand=True)
    df_rq4['Telefone'] = df_rq4['Telefone'].str.replace('-', '')
    df_rq4[['Login','Ramal']] = df_rq4['Agente'].str.split('.', expand=True)
    df_rq4['Resultado'] = df_rq4['Resultado'].str.replace(' ', '', n=1)
    df_rq4 = df_rq4.drop(columns=['CPF', 'Ficha No.', 'Data/Hora', 'Tel', 'Agente'])
    df_rq4['Data'] = pd.to_datetime(df_rq4['Data'], format='%d/%m/%Y', errors='coerce')
    df_rq4['Ducarao_segundos'] = 0

    for linha in tqdm(df_rq4.itertuples(), total=df_rq4.shape[0]):
        df_rq4['Ducarao_segundos'][linha.Index] = (int(linha.Duracao[0:2]) * 60 * 60 ) + (int(linha.Duracao[3:5]) * 60) + int(linha.Duracao[6:8])
        if linha.Hora[0:2] == '20':
            df_rq4['Hora'][linha.Index] = '19:56:56'

    for linha in tqdm(df_rq4.itertuples(), total=df_rq4.shape[0]):
        try:
            conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='flix', password='SRV.flixdb1103@')
            cursor = conexao.cursor()
            inserir_dados = f"insert into tbl_chamada (data_chamada, hora, lote, resultado, duracao, duracao_segundos ,ramal, ddd_tel, tel_cliente, cpf) values ('{linha.Data}', '{linha.Hora}', '{linha.Lote}', '{linha.Resultado}', '{linha.Duracao}', '{linha.Duracao_segundos}', '{linha.Ramal}', {linha.DDD}, {linha.Telefone}, {linha.Codigo})"
            cursor.execute(inserir_dados)
            conexao.commit()
        except Error as erro:
            logging.info(f"Falha ao inserir RQ4 do dia {data_formatada} as {hora_bot}\nErro:{erro}\nlinha: {linha}\n")
        finally:
            if(conexao.is_connected()):
                conexao.close()
                cursor.close
    msg = f'Os dados da tabela RQ4 das {hora_bot} horas foram inseridos no banco com sucesso '
    send_message(token, chat_id, msg)
except Exception  as e:
    msg = f'Ocorreu o seguinte erro durante a inserção dos dados ta tabela RQ4 das {hora_bot} horas: {e.args}'
    send_message(token, chat_id, msg)

########################################################################################### HC1 ###########################################################################################

driver.refresh() 
sleep(2)

driver.find_element(By.XPATH, '//*[@id="top5"]/a').click()
sleep(1)
driver.find_element(By.XPATH, '//*[@id="headmenu5"]/ul/li[4]/a/i').click()
sleep(1)
driver.find_element(By.XPATH, '//*[@id="lat100"]/a').click()
sleep(2)

pyautogui.click(458, 352) # Periodo
pyautogui.click(437, 389) # Hoje
pyautogui.click(458, 352) # Periodo
pyautogui.click(441, 572) # Selecione
pyautogui.click(679, 640) # Seta Selecionar Hora
pyautogui.click(677, 617) # Rolar Barra Hora

while True:
    try:
        if pyautogui.locateCenterOnScreen(hora_atual):
            hora_selecionada = pyautogui.locateCenterOnScreen(hora_atual)
            moveTo(hora_selecionada)
            click()
            break
    except:
        pass

pyautogui.click(740, 640) # Seta Selecionar Minuto
pyautogui.click(714, 341) # Selecioar Minuto
pyautogui.click(957, 640) # Seta Selecionar Hora Limite

while True:
    try:
        if pyautogui.locateCenterOnScreen(hora_limite):
            hora_selecionada = pyautogui.locateCenterOnScreen(hora_limite)
            moveTo(hora_selecionada)
            click()
            break
    except:
        pass

pyautogui.click(1017, 641) # Seta Selecionar Minuto Limite
pyautogui.click(1019, 570) # Clicar Barra Minuto Limite
pyautogui.scroll(500)
pyautogui.click(991, 326) # Selecionar Minuto Limite
pyautogui.click(1078, 682) # Aplica Hora

caminho_arquivo = r'.\Imagens\Filas'
for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
    for arquivo in arquivos:
        sleep(1)
        pyautogui.click(455, 314) # Selecionar Fila
        fila = f'.\\Imagens\\Filas\\{arquivo}'
        while True:
                try:
                    if pyautogui.locateCenterOnScreen(fila):
                        seleciona_fila = pyautogui.locateCenterOnScreen(fila)
                        moveTo(seleciona_fila)
                        click()
                        break
                except:
                    pass
        pyautogui.click(572, 591) # CSV 
        while True:
                    try:
                        if pyautogui.locateCenterOnScreen(confimacao):
                            fechar = pyautogui.locateCenterOnScreen(reset)
                            moveTo(fechar)
                            click()
                            break 
                    except:
                        pass 
        driver.switch_to.window(driver.window_handles[0])             

caminho_arquivo = r'C:\Users\Administrator\Downloads'
nome = 'HC1'
df_hc1 = pd.DataFrame()
for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
    for arquivo in arquivos:
        if nome in arquivo:
            caminho_completo = os.path.join(raiz, arquivo)
            hc1 = (caminho_completo)   
            df_concat = pd.read_csv(hc1, encoding='ISO-8859-1', sep=';', on_bad_lines='skip')
            df_hc1 = pd.concat([df_hc1, df_concat], ignore_index=True)
            os.remove(hc1)  
df_hc1.rename(columns={'ï»¿Horario':'Horario', 'Agentes que perderam toque':'Agentes_Perderam_toque', 'Agente que atendeu':'Agente_atendeu',
                    'Tempo de Fila':'Tempo_Fila', 'Tempo de Atendimento':'Tempo_Atendimento', 'Desligada por':'Desligada_por',
                    'Transbordo Status':'Transbordo_Status', 'Transbordo Tipo':'Transbordo_Tipo', 'Transbordo Destino':'Transbordo_Destino'}, inplace=True)
df_hc1[['Data','Hora']] = df_hc1['Horario'].str.split(' ', expand=True) 
df_hc1[['Login','Ramal']] = df_hc1['Agente_atendeu'].str.split('.', expand=True)
df_hc1 = df_hc1.drop(columns=['Agente_atendeu'])
df_hc1['Data'] = pd.to_datetime(df_hc1['Data'], format='%d/%m/%Y', errors='coerce')
df_hc1['Duracao_segundos'] = 0

for linha in tqdm(df_hc1.itertuples(), total=df_hc1.shape[0]):
    if linha.Tempo_Atendimento != '-':
        try:
            df_hc1['Duracao_segundos'][linha.Index] = (int(linha.Tempo_Atendimento[0:2]) * 60 * 60 ) + (int(linha.Tempo_Atendimento[3:5]) * 60) + int(linha.Tempo_Atendimento[6:8])
        except:
            pass
    elif linha.Tempo_Atendimento == '-':
        df_hc1['Duracao_segundos'][linha.Index] = ''
    try:
        if linha.Hora[0:2] == '20':
            try:
                df_hc1['Hora'][linha.Index] = '19:56:56'
            except:
                pass
    except:
        pass

for linha in tqdm(df_hc1.itertuples(), total=df_hc1.shape[0]):
    if linha.Ramal != None:
        try:
            conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
            cursor = conexao.cursor()
            inserir_dados = f"insert into tbl_desliga (telefone, data, hora, duracao, duracao_segundos ,desligado, ramal) values ('{linha.Numero}', '{linha.Data}', '{linha.Hora}','{linha.Tempo_Atendimento}', '{linha.Duracao_segundos}', '{linha.Desligada_por}', '{linha.Ramal}')"
            cursor.execute(inserir_dados)
            conexao.commit()
        except Error as erro:
            logging.info(f"Falha ao inserir HC1 do dia {data_formatada} as {hora_bot}\nErro:{erro}\nlinha: {linha}\n")
        finally:
            if(conexao.is_connected()):
                conexao.close()
                cursor.close
msg = f'Os dados da tabela HC1 das {hora_bot} horas foram inseridos no banco com sucesso '
send_message(token, chat_id, msg)

########################################################################################### Agilus ###########################################################################################

sleep(2)
pyautogui.PAUSE = 3.5

try:
    pyautogui.press('winleft')
    pyautogui.write('agilus')
    #sleep(1)
    pyautogui.press('enter')
    sleep(3)
    pyautogui.write('02121997Law')  
    pyautogui.press('enter')
    pyautogui.press('enter')
    sleep(3)
    pyautogui.click(106, 35) # Relatorios
    pyautogui.click(134, 814) # Extração AF
    pyautogui.click(415, 335) # Data inicio
    pyautogui.write(data_formatada)
    pyautogui.click(513, 334) # Data final
    pyautogui.write(data_formatada)
    pyautogui.click(431, 490) # Visualizar Relatorio
    pyautogui.click(82, 39) # Export
    pyautogui.click(125, 217) # CSV File
    pyautogui.press('enter')

    sleep(2)
    pyautogui.write(f'MetaHora_{hora}h')
    sleep(2)
    pyautogui.press('enter')
    pyautogui.click(1411, 6)
    pyautogui.click(1411, 6)

    caminho_arquivo = r'C:\Users\Administrator\Documents'
    nome = 'MetaHora'
    for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
        for arquivo in arquivos:
            if nome in arquivo:
                caminho_completo = os.path.join(raiz, arquivo)
                agilus = (caminho_completo)
    df_agilus = pd.read_csv(agilus, encoding='ISO-8859-1', sep=';', thousands = '.', decimal = ',', dtype = {'VALOR_PARCELA':np.float64})
    os.remove(agilus)

    df_agilus[['Data','Hora']] = df_agilus['DATA CADASTRAMENTO'].str.split(' ', expand=True)
    df_agilus = df_agilus[['CÓD.AF', 'RAMAL', 'CPF','Data', 'Hora', 'VALOR PARCELA', 'FASE']]
    df_agilus = df_agilus.rename(columns={'VALOR PARCELA': 'VALOR_PARCELA', 'CÓD.AF':'COD_AF'})
    df_agilus['Data'] = pd.to_datetime(df_agilus['Data'], format='%d/%m/%Y', errors='coerce')

    for linha in tqdm(df_agilus.itertuples(), total=df_agilus.shape[0]):
        if linha.Hora[0:2] == '20':
            df_agilus['Hora'][linha.Index] = '19:56:56'

    for linha in tqdm(df_agilus.itertuples(), total=df_agilus.shape[0]):
        try:
            conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='flix', password='SRV.flixdb1103@')
            cursor = conexao.cursor()
            inserir_dados = f"insert into tbl_venda (cod_af, data, hora, valor_parcela, fase, cpf, ramal) values ('{linha.COD_AF}', '{linha.Data}', '{linha.Hora}', '{linha.VALOR_PARCELA}', '{linha.FASE}', {linha.CPF}, {linha.RAMAL})"
            cursor.execute(inserir_dados)
            conexao.commit()
        except Error as erro:
            logging.info(f"Falha ao inserir Agilus do dia {data_formatada} as {hora_bot}\nErro:{erro}\nlinha: {linha}\n")
        finally:
            if(conexao.is_connected()):
                conexao.close()
                cursor.close
    msg = f'Os dados do Agilus das {hora_bot} horas foram inseridos no banco com sucesso '
    send_message(token, chat_id, msg)
except Exception  as e:
    msg = f'Ocorreu o seguinte erro durante a inserção dos dados do Agilus das {hora_bot} horas: {e.args}'
    send_message(token, chat_id, msg)

msg = f'Todos os dados da discadora e do agilus das {hora_bot} horas foram inseridos no banco com sucesso '
send_message(token, chat_id, msg)

########################################################################################### TAQ1 ###########################################################################################


########################################################################################### PA1 ###########################################################################################

url = "https://maisvoip488.ipboxcloud.com.br:8944/ipbox/api/getPA1"

try:
    if mes >= 10:
        payload=f'de={ano}{mes}{dia}000000&ate={ano}{mes}{dia}235959'
    else:
        payload=f'de={ano}0{mes}{dia}000000&ate={ano}0{mes}{dia}235959'

    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC92ZXJpeC5jb20uYnIiLCJhdWQiOiJodHRwOlwvXC9pcGJveC5jb20uYnIiLCJpYXQiOjE2NTcwMjc3NTMsIm5iZiI6MTY1NzAyNzc1NSwiZGF0YSI6eyJ1c3VhcmlvX2lkIjoiMSIsInRva2VuX2lkIjoiYkdpY1pxQzVVZUxHNEVydVlESlUifX0.h2f-fVil0x14O2vTsR-IzOhlei2o4Lf9GYxWo8C59i8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pa1 = response.json()

    conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
    cursor = conexao.cursor()
    deletar_dados = f"delete from tbl_tempo_logado where data = '{data_registro}'"
    cursor.execute(deletar_dados)
    conexao.commit()

    for registro in tqdm(pa1['data']):
        if registro['tempo_logado'] != '-' and registro['agente'] != 'TOTAIS':
            t_logado_segundos = (int(registro['tempo_logado'][0:2]) * 60 * 60 ) + (int(registro['tempo_logado'][3:5]) * 60) + int(registro['tempo_logado'][6:8])
        elif registro['tempo_logado'] == '-':
            t_logado_segundos = ''
        agente = registro['agente'].split('.')

        if registro['tempo_logado'] != '-' and registro['agente'] != 'TOTAIS':
            try:
                conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
                cursor = conexao.cursor()
                inserir_dados = f"insert into tbl_tempo_logado (tempo_logado,tempo_logado_segundos, data, tbl_agente_ramal) values ('{registro['tempo_logado']}', '{t_logado_segundos}','{data_registro}', '{agente[1]}')"
                cursor.execute(inserir_dados)
                conexao.commit()
            except Error as erro:
                logging.info(f"Falha ao inserir Tempo Logado do dia {data_formatada} as {hora_bot}\nErro:{erro}\nlinha: {registro}\n")
            finally:
                if(conexao.is_connected()):
                    conexao.close()
                    cursor.close
    msg = f'Os dados PA1 das {hora_bot} horas foram inseridos no banco com sucesso '
    send_message(token, chat_id, msg)
except Exception  as e:
    msg = f'Ocorreu o seguinte erro durante a inserção dos dados PA1 das {hora_bot} horas: {e.args}'
    send_message(token, chat_id, msg)

########################################################################################### Pausas ###########################################################################################

url = "https://maisvoip488.ipboxcloud.com.br:8944//ipbox/api/getPausaAgente"

try:
    if mes >= 10:
        payload=f'de={ano}-{mes}-{dia}%20{hora}%3A01%3A00&ate={ano}-{mes}-{dia}%20{hora_bot}%3A59%3A59&'
    else:
        payload=f'de={ano}-0{mes}-{dia}%20{hora}%3A01%3A00&ate={ano}-0{mes}-{dia}%20{hora_bot}%3A59%3A59&'
    headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC92ZXJpeC5jb20uYnIiLCJhdWQiOiJodHRwOlwvXC9pcGJveC5jb20uYnIiLCJpYXQiOjE2NTcwMjc3NTMsIm5iZiI6MTY1NzAyNzc1NSwiZGF0YSI6eyJ1c3VhcmlvX2lkIjoiMSIsInRva2VuX2lkIjoiYkdpY1pxQzVVZUxHNEVydVlESlUifX0.h2f-fVil0x14O2vTsR-IzOhlei2o4Lf9GYxWo8C59i8',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pausas = response.json()

    def remove_repetidos(lista_pausas):
        l = []
        for i in tqdm(lista_pausas):
            if i not in l:
                l.append(i)
        return l

    lista_pausas = pausas['data']
    lista_pausas = remove_repetidos(lista_pausas)

    conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
    cursor = conexao.cursor()
    deletar_dados = f"delete from tbl_pausa where data = '{data_registro}'"
    cursor.execute(deletar_dados)
    conexao.commit()

    for pausa in tqdm(lista_pausas): 
        try:
            conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
            cursor = conexao.cursor()       
            data = datetime.strptime(pausa['data'][:10], '%d/%m/%Y').date()
            hora_pausa = pausa['data'][11:]
            if hora_pausa[0:2] == '20':
                hora_pausa = '19:56:56'
            motivo = pausa['motivo']
            duracao = pausa['duracao']
            duracao_segundos = (int(duracao[0:2]) * 60 * 60 ) + (int(duracao[3:5]) * 60) + int(duracao[6:8])
            agente = pausa['agente'].split('.')
            inserir_dados = f"insert into tbl_pausa (motivo, duracao, duracao_segundos ,data, hora_pausa, tbl_agente_ramal) values ('{motivo}','{duracao}','{duracao_segundos}','{data}','{hora_pausa}','{agente[1]}')"
            cursor.execute(inserir_dados)
            conexao.commit()
        except Error as erro:
            logging.info(f"Falha ao inserir Pausas do dia {data_formatada} as {hora_bot}\nErro:{erro}\nlinha: {pausa}\n")
        finally:
            if(conexao.is_connected()):
                conexao.close()
                cursor.close
    msg = f'Os dados Pausas das {hora_bot} horas foram inseridos no banco com sucesso '
    send_message(token, chat_id, msg)
except Exception  as e:
    msg = f'Ocorreu o seguinte erro durante a inserção dos dados Pausas das {hora_bot} horas: {e.args}'
    send_message(token, chat_id, msg)

driver.quit()