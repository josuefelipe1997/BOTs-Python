import time
from numpy import int64
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

t = 0
usuario = input('Usuário: ')
senha = input('Senha: ')
tronco_maximo = int(input('Qual o valor MÁXIMO de troncos: '))
tronco_minimo = int(input('Qual o valor MÍNIMO de troncos: '))
aux = int(input('Quantas filas deseja adicionas: '))
filas = []
c = 1
while True:
    txt = str(input(f'Digite o codigo da {c}° fila que deseja alterar: '))    
    filas.append(txt)
    c += 1
    if(len(filas) == aux ):
        break
tempo = int(input('Quantos segundos entre cada verificação: '))
# Função que vai até a até a pagina onde os troncos precisam ser mudados, verifica o valor atual dos troncos e de acordo com as condições realiza as ações
def Troncos():
    url_fila = 'http://192.168.11.5/admin/queues'
    driver.get(url_fila)
    driver.find_element_by_xpath(var_xpath).click()
    time.sleep(1)
    # Verifica se o numero de pessoas disponiveis por mais de 40 segundos é maior do que a metade dos agentes, caso seja aumenta o tronc
    if(aux >= (agente / 2)):
        troncos = driver.find_element(By.XPATH, '//*[@id="dialer_max_trunks"]')
        attrs=[]
        # For que varre o HTML pegando os atributos para saber o valor atual do tronco
        for attr in troncos.get_property('attributes'):
            attrs.append([attr['name'], attr['value']])
        tronco = int(attrs[5][1])
        # Verifica se o valor do tronco é menor que 25, caso seja aumenta o tronco em 2
        if(tronco < tronco_maximo):
            tronco += 2
            driver.find_element_by_xpath('//*[@id="dialer_max_trunks"]').clear()
            driver.find_element_by_xpath('//*[@id="dialer_max_trunks"]').send_keys(tronco)
            confirmar = driver.find_element_by_xpath('//*[@id="queue"]/div[5]/input[2]').click()
            print(f'O novo valor do tronco é {tronco}')      
        else:
            print(f'Tronco já esta no valor maximo de {tronco_maximo}')
    # Verifica se a fila de espera é maior do que 3
    elif(int64(espera) >= 3):
        troncos = driver.find_element(By.XPATH, '//*[@id="dialer_max_trunks"]')
        attrs=[]
        for attr in troncos.get_property('attributes'):
            attrs.append([attr['name'], attr['value']])
        tronco = int(attrs[5][1])
        # Verifica se o valor do tronco é maior que 8, caso seja diminui o tronco em 2
        if(tronco > tronco_minimo):
            tronco -= 2
            driver.find_element_by_xpath('//*[@id="dialer_max_trunks"]').clear()
            driver.find_element_by_xpath('//*[@id="dialer_max_trunks"]').send_keys(tronco)
            confirmar = driver.find_element_by_xpath('//*[@id="queue"]/div[5]/input[2]').click()
            print(f'O novo valor do tronco é {tronco}')
        else:
            print(f'Tronco já esta no valor minimo de {tronco_minimo}') 

# Acessa o Site e faz o login
url = 'http://192.168.11.5/'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', options=options)
driver.get(url)
user = driver.find_element_by_name('username')
user.send_keys(usuario)
pas = driver.find_element_by_name('password')
pas.send_keys(senha)
login = driver.find_element_by_name('commit').click()

# Loop infinito para que o programa fique rodando
while t < 12:
    # Pega a tabela onde os agentes vão ficar sendo verificados e pega quantas ligações estão na fila de espera
    df = pd.read_html(driver.find_element_by_xpath('//*[@id="14250_datagrid_wrapper"]').get_attribute('outerHTML'))[0]
    df['Duração'] = df['Duração'].replace({'m':'', 's':'', ' ':'', '-':'0'}, regex=True)
    df_espera = pd.read_html(driver.find_element_by_xpath('//*[@id="auxiliarcontent"]/table[2]').get_attribute('outerHTML'))[0]
    espera = df_espera['Discadas.1'][6]
    
    count = 0
    aux = 0
    agente = 0

    # Verifica quantos agentes tem disponivel por mais de 40 segundos
    for i in df['Agente']:
        if((df['Status'][count] == 'Disponivel') and (int64(df['Duração'][count]) > 40)):
            aux = aux + 1
        agente = agente + 1
        count = count + 1
    print(f'{aux} pessoas disponiveis por mais de 40 segundos')  
    print(f'{espera} chamadas na fila de espera')
    # Verifica se o numero de agentes e maior do que 5
    if(agente > 5):
        # Verifica se o numero de pessoas disponiveis por mais de 40 segundos é maior do que a metade dos agentes, caso seja aumenta o tronco
        if(aux >= (agente / 2)):
            for i in filas:
                var_xpath = f'//*[@id="queue_{i}"]/td[5]'
                Troncos()
                print(f'Tronco da fila {i} alterado')
            print('Os troncos foram aumentados')
        # Verifica se a fila de espera é maior que 3, caso seja diminui o tronco
        elif(int64(espera) >= 3):
            for i in filas:
                var_xpath = f'//*[@id="queue_{i}"]/td[5]'
                Troncos()
                print(f'Tronco da fila {i} alterado')
            print('Os troncos foram diminuidos')
        else:
            print('Fluxo de ligações OK')
    else:
        print('Não tem mais do que 5 agentes logados')
    print('')
    driver.get(url)
    time.sleep(tempo)
driver.quit()