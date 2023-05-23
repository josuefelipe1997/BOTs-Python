import pandas as pd
import os
from tkinter.filedialog import askopenfile
from tkinter import Tk

Tk().withdraw()
filename = askopenfile()

df_dados = pd.read_csv(filename, encoding='ISO-8859-1', sep=';') 
vezes = int(len(df_dados) / 50000)
tamanho = int(len(df_dados) / vezes)

for vez in range(vezes):
    if vez == 0:
        df_parte = df_dados.loc[(df_dados.index < tamanho)]
        df_parte = df_parte.reindex(columns = ['CPF', 'BENEFICIO', 'NOME', 'TELEFONE1', 'TELEFONE2', 'TELEFONE3', 'TELEFONE4', 'TELEFONE5'])
        df_parte.to_csv((f'.\Digitos\Digito_9\{vez}.csv'), sep=';', index=False)
    elif vez >= 1:
        df_parte = df_dados.loc[(df_parte.index + tamanho)]
        df_parte = df_parte.reindex(columns = ['CPF', 'BENEFICIO', 'NOME', 'TELEFONE1', 'TELEFONE2', 'TELEFONE3', 'TELEFONE4', 'TELEFONE5'])
        df_parte.to_csv((f'.\Digitos\Digito_9\{vez}.csv'), sep=';', index=False)
