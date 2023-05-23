import pandas as pd
import os
from tkinter.filedialog import askdirectory
from tkinter import Tk

Tk().withdraw()
caminho_arquivo = askdirectory()
nome = 'HC1'

df_discagens = pd.DataFrame()

for raiz, diretorios, arquivos in os.walk(caminho_arquivo):
    for arquivo in arquivos:
        print(arquivo)
        caminho_completo = os.path.join(raiz, arquivo)
        df_concat = pd.read_csv(caminho_completo, encoding='ISO-8859-1', sep=';')
        df_discagens = pd.concat([df_discagens, df_concat], ignore_index=True)
        
df_discagens.to_csv((f'HC1.csv'), sep=';', index=False)