import time
import datetime
from selenium import webdriver

turno_manha_vonix = {1:'50006', 2:'00021', 3:'00075', 4:'00026', 5:'00046', 6:'00056', 7:'00053', 8:'50007', 9:'50008', 10:'00054', 11:'50009', 12:'00070'}
turno_manha_maisvoip = {1:'6028', 2:'6003', 3:'6002', 4:'6016', 5:'6004', 6:'6005', 7:'6027', 8:'6029', 9:'6030', 10:'6001', 11:'6031', 12:'6014'}

turno_tarde_vonix = {1:'00031', 2:'00076', 3:'00071', 4:'50001', 5:'00078', 6:'50002', 7:'00079', 8:'50003', 9:'00072', 10:'0', 11:'50004', 12:'50005'}
turno_tarde_maisvoip = {1:'6007', 2:'6008', 3:'6009', 4:'6022', 5:'6010', 6:'6023', 7:'6011', 8:'6024', 9:'6012', 10:'0', 11:'6025', 12:'6026'}
 
url = 'https://sistemavanguard.app/vanguard/index.php/funcionario'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')#, options=options
driver.get(url)
time.sleep(1)

driver.find_element_by_xpath('//*[@id="exten"]').send_keys('flix.aux@5433')
driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/div/input').send_keys('Senha@aux')
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
time.sleep(1)

driver.get(url)
time.sleep(1)

while True:
    try:
        discadora = 1 #int(input('\n1 - Vonix\n2 - Mais Voip\n\nDeseja mudar para qual discadora: '))
        if discadora == 1 or discadora == 2:
            break
        else:
            print('Opção invalida, tente novamente !!!')
    except:
        print('Por favor, digite um valor valido !!!')
        
data = datetime.datetime.now()
hora_atual = (str(data.hour))
hora_atual = (int(hora_atual))

if (hora_atual < 14 ):
    if discadora == 1:
        turno = turno_manha_vonix
    elif discadora == 2:
        turno = turno_manha_maisvoip      
elif(hora_atual >= 14):
    if discadora == 1:
        turno = turno_tarde_vonix
    elif discadora == 2:
        turno = turno_tarde_maisvoip  
         
for key in turno.keys():
    driver.find_element_by_xpath(f'//*[@id="tblExport"]/tbody/tr[{key}]/td[9]/a[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="ramal"]').clear()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="ramal"]').send_keys(turno[key])
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="frmfuncionario"]/div/div/div/div[7]/div/button').click()
    print('Troca realizada com sucesso !!!')
    time.sleep(2)
    
driver.quit()