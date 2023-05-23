import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

farm = ['-85,2', '-84,-4', '-84,-5', '-82,-4', '-81,-4', '-86,-4']

url_travian = 'https://nys.x1.america.travian.com/dorf1.php'
url_ponto_reuniao = 'https://nys.x1.america.travian.com/build.php?id=39&gid=16&tt=2'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options
driver.get(url_travian)
driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/form/table/tbody/tr[1]/td[2]/input').send_keys('USUARIO')
driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/form/table/tbody/tr[2]/td[2]/input').send_keys('SENHA')
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="s1"]').click()
i = 0
while True:
    driver.get(url_travian)
    time.sleep(2) 
       
    if i > len(farm):
        i = 0  
                 
    x = farm[i][0:3]
    y = farm[i][4:]
    
    df_tropas = pd.read_html(driver.find_element_by_id("troops").get_attribute('outerHTML'))[0] 
                              
    if df_tropas['Tropas:.2'][0] == 'Herói':
        driver.get(url_ponto_reuniao)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[3]/td[4]/a').click()
        driver.find_element(By.XPATH, '//*[@id="xCoordInput"]').send_keys(x)
        driver.find_element(By.XPATH, '//*[@id="yCoordInput"]').send_keys(y)
        driver.find_element(By.XPATH, '//*[@id="build"]/div/form/div[2]/label[3]/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="btn_ok"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="btn_ok"]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="build"]/div[2]/table[1]/thead/tr/td[2]/a/span').click()
        time.sleep(1)
        
        df_inimigos = pd.read_html(driver.find_element_by_id("troop_info").get_attribute('outerHTML'))[0]  
           
        if df_inimigos[0][0] == 'nenhum':
            i+=1
            driver.get('https://nys.x1.america.travian.com/build.php?id=39&gid=16&tt=1')
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="build"]/div[2]/table[1]/tbody[3]/tr/td/div[2]/button').click()
            time.sleep(10)
            
    elif df_tropas['Tropas:.2'][0] != 'Herói':
        print('Heroi não esta na vila!!!')
        time.sleep(300)