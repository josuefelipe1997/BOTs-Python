import os
import datetime

data = datetime.datetime.now()
ano_atual = int(data.year)

pasta = input('\nColoque o caminho para a pasta:\n-> ')
padrao = '(Seg|seg|SEG)_(52077|52300|5273|1679|54538)_(\d\d\d\d\d\d\d\d\d\d\d)_(\d\d\d\d\d\d\d\d\d\d\d\d\d\d)_1_1_(\d\d\d\d\d\d\d\d)\.mp3'
nao_padronizados = []
padronizados = []	
splitados = []

for arquivo in os.listdir(pasta):
    for arquivos in arquivo:
        splitados.append(arquivo.split('_'))
        for item in splitados:
            verificador = []
            for letra in item[3]:                
                verificador.append(letra)                                                            
    ano = ''.join(map(str, verificador[0:4]))
    mes = ''.join(map(str, verificador[4:6]))
    dia = ''.join(map(str, verificador[6:8]))
    hora = ''.join(map(str, verificador[8:10]))
    min = ''.join(map(str, verificador[10:12]))
    sec = ''.join(map(str, verificador[12:14])) 
                                  
    check = 0               
    if int(ano) == ano_atual:
        check += 1   
    if (int(mes) < 13) and (int(mes) > 0):
        check += 1    
    if (int(dia) <= 31) and (int(dia) > 0):
        check += 1
    if (int(hora) <= 24) and (int(hora) >= 00):
        check += 1
    if (int(min) <= 59) and (int(hora) >= 00):
        check += 1   
    if (int(sec) <= 59) and (int(sec) >= 00):
        check += 1
                           
    if check == 6:
        padronizados.append(arquivo)
    else:
        nao_padronizados.append(arquivo)
      
if len(nao_padronizados) == 0:
	print ('\n[ * ] Todos os arquivos estão com a sintaxe correta !')
	pause = input('\nPressione <Enter> para finalizar...')
	exit()
if len(nao_padronizados) > 0:
	print ('\n[ ! ] Foram encontrados {} arquivos com a sintaxe fora do padrão:\n'.format(len(nao_padronizados)))
	for arquivo in nao_padronizados:
		print (arquivo)
	pause = input('\nPressione <Enter> para finalizar...')
	exit() 
