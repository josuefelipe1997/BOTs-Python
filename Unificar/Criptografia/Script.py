from cmath import nan
from numpy import nan_to_num
import pandas as pd
import os
from pandas.io.parsers import read_csv
from tkinter.filedialog import askdirectory
from tkinter import Tk

from sqlalchemy import null

Tk().withdraw()

df_vanguard = pd.DataFrame()
filename = askdirectory()
nome = 'apiAddMailing'
            
for raiz, diretorios, arquivos in os.walk(filename):
    for arquivo in arquivos:
        if nome in arquivo:
            caminho_completo = os.path.join(raiz, arquivo)
            df_arquivos = pd.read_csv(caminho_completo, encoding='ISO-8859-1', sep='|') 
            df_vanguard = pd.concat([df_vanguard, df_arquivos], ignore_index=True)
          
df_vanguard['codigo'] = df_vanguard['codigo'].replace({'c':'', 'G':'0', 'J':'1', 'D':'2','W':'3', 'Z':'4',
                                                       'S':'5', 'T':'6', 'O':'7', 'H':'8', 'C':'9'}, regex=True)

df_vanguard = df_vanguard.dropna(subset=['ddd1'])
df_vanguard.reset_index(drop=True)

for coluna in df_vanguard.columns:
    if coluna != 'acao' and coluna != 'nome' and coluna != 'codigo':
        df_vanguard[str(coluna)] = df_vanguard[str(coluna)].astype('float64')
        df_vanguard[str(coluna)] = df_vanguard[str(coluna)].astype('Int64')
        
df_vanguard.drop(['acao'], axis='columns', inplace=True)
df_vanguard.to_csv((f'{filename}\Descriptografado.csv'), sep=';', index=False)

exit = input('\n\nO ARQUIVO FOI DESCRIPTOGRAFADO, PRESSIONE ENTER PARA TERMINAR#')