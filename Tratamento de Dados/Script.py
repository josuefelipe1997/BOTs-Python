import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from copy import error
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def google_sheets(SAMPLE_SPREADSHEET_ID):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
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
                                range=f'{celula}!A1:Z').execute()
    values = result.get('values', [])
    df_sheets = pd.DataFrame(values)
    df_sheets = df_sheets.rename(columns=df_sheets.iloc[0]).loc[1:]
    return df_sheets

########################################################################################### Auditoria ###########################################################################################

SAMPLE_SPREADSHEET_ID = '1iyImH2N2g3x-miZ09ebrvLb2mjWZH93W-tPI72Iy3_8'
celula = 'DATABASE'
df_auditoria = google_sheets(SAMPLE_SPREADSHEET_ID)

df_auditoria[['DATA','HORA']] = df_auditoria['DATA CADASTRAMENTO'].str.split(' ', expand=True)
df_auditoria = df_auditoria[['DATA', 'CPF', 'STATUS', 'MOTIVO', 'COD.AF', 'RAMAL']]
df_auditoria['DATA'] = pd.to_datetime(df_auditoria['DATA'], format='%d/%m/%Y')
df_auditoria.rename(columns={'COD.AF':'COD_AF'}, inplace=True)
df_auditoria = df_auditoria.dropna()
df_auditoria['CPF'] = df_auditoria['CPF'].str.replace('.','', regex=True)
df_auditoria['CPF'] = df_auditoria['CPF'].str.replace('-','', regex=True)
df_auditoria['CPF'] = df_auditoria['CPF'].astype('int64')
df_auditoria['COD_AF'] = df_auditoria['COD_AF'].astype('int64')

for linha in tqdm(df_auditoria.itertuples(), total=df_auditoria.shape[0]):
    conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
    cursor = conexao.cursor()
    try:
        inserir_dados = f'insert into tbl_auditoria (cod_af, data, status, motivo, tbl_agente_ramal, tbl_cliente_cpf) values ({linha.COD_AF}, "{linha.DATA}", "{linha.STATUS}", "{linha.MOTIVO}" , {linha.RAMAL}, {linha.CPF})'
        cursor.execute(inserir_dados)
        conexao.commit()
    except Error as erro:
        update_dados = f'update tbl_auditoria set data="{linha.DATA}",status="{linha.STATUS}",motivo="{linha.MOTIVO}",tbl_agente_ramal={linha.RAMAL},tbl_cliente_cpf={linha.CPF} where cod_af={linha.COD_AF}'
        cursor.execute(update_dados)
        conexao.commit()
    finally:
        if(conexao.is_connected()):
            conexao.close()
            cursor.close

########################################################################################### Edição/Gravação ###########################################################################################

SAMPLE_SPREADSHEET_ID = '1u5zIOvuUr9ZEotkP7QR6iy5B9eWjKhTHeUgY78rRtGM'
celula = 'DATABASE'
df_gravacao = google_sheets(SAMPLE_SPREADSHEET_ID)

df_gravacao[['DATA','HORA']] = df_gravacao['DATA'].str.split(' ', expand=True)
df_gravacao = df_gravacao[['DATA', 'CPF', 'STATUS', 'MOTIVO', 'AUDITOR','COD AF', 'RAMAL']]
df_gravacao['CPF'] = df_gravacao['CPF'].str.replace('.','', regex=True)
df_gravacao['CPF'] = df_gravacao['CPF'].str.replace('-','', regex=True)
df_gravacao['CPF'] = df_gravacao['CPF'].astype('int64')
df_gravacao['DATA'] = pd.to_datetime(df_gravacao['DATA'], format='%d/%m/%Y')
df_gravacao.rename(columns={'COD AF':'COD_AF'}, inplace=True)
df_gravacao = df_gravacao.dropna()

for linha in tqdm(df_gravacao.itertuples(), total=df_gravacao.shape[0]):
    conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
    cursor = conexao.cursor()
    try:
        inserir_dados = f'insert into tbl_gravacao (cod_af, data, status, motivo, auditor,tbl_agente_ramal, tbl_cliente_cpf) values ({linha.COD_AF}, "{linha.DATA}", "{linha.STATUS}", "{linha.MOTIVO}", "{linha.AUDITOR}", {linha.RAMAL}, {linha.CPF})'
        cursor.execute(inserir_dados)
        conexao.commit()
    except Error as erro:
        update_dados = f'update tbl_gravacao set data="{linha.DATA}",status="{linha.STATUS}",motivo="{linha.MOTIVO}", auditor="{linha.AUDITOR}",tbl_agente_ramal={linha.RAMAL}, tbl_cliente_cpf={linha.CPF} where cod_af={linha.COD_AF}'
        print(update_dados)
        cursor.execute(update_dados)
        conexao.commit()
    finally:
        if(conexao.is_connected()):
            conexao.close()
            cursor.close

########################################################################################### Analise Pendente ###########################################################################################

SAMPLE_SPREADSHEET_ID = '1d2TttKEi8D4akzblTp7MhRrfJW5Sh0-Tefgv7GMo1hs'
celula = 'DATABASE'
df_analise_pendente = google_sheets(SAMPLE_SPREADSHEET_ID)
df_analise_pendente[['DATA','HORA']] = df_analise_pendente['DATA'].str.split(' ', expand=True)
df_analise_pendente = df_analise_pendente[['DATA', 'CPF', 'STATUS', 'MOTIVO', 'AUDITOR', 'RAMAL']]
df_analise_pendente['DATA'] = pd.to_datetime(df_analise_pendente['DATA'], format='%d/%m/%Y', errors='coerce')
df_analise_pendente['CPF'] = df_analise_pendente['CPF'].str.replace('.','', regex=True)
df_analise_pendente['CPF'] = df_analise_pendente['CPF'].str.replace('-','', regex=True)

for linha in tqdm(df_analise_pendente[::-1].itertuples(), total=df_analise_pendente.shape[0]):
    if linha.CPF != '':
        try:
            conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
            cursor = conexao.cursor()
            inserir_dados = f'insert into tbl_analise (data, status, motivo, auditor, tbl_agente_ramal, tbl_cliente_cpf) values ("{linha.DATA}", "{linha.STATUS}", "{linha.MOTIVO}", "{linha.AUDITOR}" , "{linha.RAMAL}", "{linha.CPF}")'
            cursor.execute(inserir_dados)
            conexao.commit()
        except Error as erro:
            print(linha)
            print(erro)
        finally:
            if(conexao.is_connected()):
                conexao.close()
                cursor.close

########################################################################################## Revisão ###########################################################################################

SAMPLE_SPREADSHEET_ID = '1cbOAvEE5UL6gAB50Gnt-w_nvGyaK_JFPDTTaAvCxvcg'
celula = 'DB REVISÃO DE PENDÊNCIA'
df_revisao_pendencia = google_sheets(SAMPLE_SPREADSHEET_ID)
df_revisao_pendencia[['DATA','HORA']] = df_revisao_pendencia['DATA CADASTRAMENTO'].str.split(' ', expand=True)
df_revisao_pendencia['DATA'] = pd.to_datetime(df_revisao_pendencia['DATA'], format='%d/%m/%Y', errors='coerce')
df_revisao_pendencia = df_revisao_pendencia[['DATA', 'CPF', 'PENDÊNCIA INCORRETA?', 'ERRO', 'RESPONSÁVEL', 'SUPERVISOR QUE VOLTOU A VENDA', 'PROCESSO', 'COD.AF']]
df_revisao_pendencia.rename(columns={'PENDÊNCIA INCORRETA?':'PENDENCIA_INCORRETA', 'RESPONSÁVEL':'RESPONSAVEL', 'SUPERVISOR QUE VOLTOU A VENDA': 'SUPERVISOR', 'COD.AF':'COD_AF'}, inplace=True)
df_revisao_pendencia['CPF'] = df_revisao_pendencia['CPF'].str.replace('.','', regex=True)
df_revisao_pendencia['CPF'] = df_revisao_pendencia['CPF'].str.replace('-','', regex=True)
df_revisao_pendencia.dropna(subset=['DATA'], inplace=True)
df_revisao_pendencia['CPF'] = df_revisao_pendencia['CPF'].astype('int64')
df_revisao_pendencia['COD_AF'] = df_revisao_pendencia['COD_AF'].astype('int64')
df_revisao_pendencia_sim = df_revisao_pendencia[df_revisao_pendencia['PENDENCIA_INCORRETA'] == 'SIM']
df_revisao_pendencia_nao = df_revisao_pendencia[df_revisao_pendencia['PENDENCIA_INCORRETA'] == 'NAO']

for linha in tqdm(df_revisao_pendencia_nao.itertuples(), total=df_revisao_pendencia_nao.shape[0]):
    try:
        conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
        cursor = conexao.cursor()
        inserir_dados = f'insert into tbl_revisao (cod_af, data, pendencia_incorreta, erro, responsavel, surpevisor, processo, tbl_cliente_cpf) values ({linha.COD_AF}, "{linha.DATA}", "{linha.PENDENCIA_INCORRETA}", "{linha.ERRO}" , "{linha.RESPONSAVEL}", "{linha.SUPERVISOR}", "{linha.PROCESSO}", {linha.CPF})'
        cursor.execute(inserir_dados)
        conexao.commit()
    except Error as erro:
        pass
    finally:
        if(conexao.is_connected()):
            conexao.close()
            cursor.close

for linha in tqdm(df_revisao_pendencia_sim.itertuples(), total=df_revisao_pendencia_sim.shape[0]):
    conexao = mysql.connector.connect(host='localhost', database='yggdrasil',user='root', password='SRV.flixdb1103@')
    cursor = conexao.cursor()
    try:    
        inserir_dados = f'insert into tbl_revisao (cod_af, data, pendencia_incorreta, erro, responsavel, surpevisor, processo, tbl_cliente_cpf) values ({linha.COD_AF}, "{linha.DATA}", "{linha.PENDENCIA_INCORRETA}", "{linha.ERRO}" , "{linha.RESPONSAVEL}", "{linha.SUPERVISOR}", "{linha.PROCESSO}", {linha.CPF})'
        cursor.execute(inserir_dados)
        conexao.commit()
        if linha.PROCESSO == 'AUDITORIA':
            update_dados_auditoria = f'update tbl_auditoria set status="OK",motivo="" where cod_af={linha.COD_AF}'
            cursor.execute(update_dados_auditoria)
            conexao.commit()
        elif linha.PROCESSO == 'GRAVACAO':
            update_dados_gravacao = f'update tbl_gravacao set status="OK",motivo="" where cod_af={linha.COD_AF}'
            cursor.execute(update_dados_gravacao)
            conexao.commit()
    except Error as erro:
        update_dados = f'update tbl_revisao set data="{linha.DATA}",pendencia_incorreta="{linha.PENDENCIA_INCORRETA}",erro="{linha.ERRO}",responsavel="{linha.RESPONSAVEL}",surpevisor="{linha.SUPERVISOR}",processo="{linha.PROCESSO}",tbl_cliente_cpf={linha.CPF} where cod_af={linha.COD_AF}'
        cursor.execute(update_dados)
        conexao.commit()
        if linha.PROCESSO == 'AUDITORIA':
            update_dados_auditoria = f'update tbl_auditoria set status="OK",motivo="" where cod_af={linha.COD_AF}'
            cursor.execute(update_dados_auditoria)
            conexao.commit()
        if linha.PROCESSO == 'GRAVACAO':
            update_dados_gravacao = f'update tbl_gravacao set status="OK",motivo="" where cod_af={linha.COD_AF}'
            cursor.execute(update_dados_gravacao)
            conexao.commit()
    finally:
        if(conexao.is_connected()):
            conexao.close()
            cursor.close