Esse projeto foi realizado com o intuito de atualizar dados de uma base de dados online, para isso é necessário que seleciona a pasta onde esses arquivos estão, o script automaticamente ira acessar o site 
onde as informações precisam ser atualizadas e subir arquivo por arquivo, cada arquivo precisa ser inserido por vez, com isso em mente após subir o primeiro arquivo, é feito uma pausa onde a tela é scaneada constantemente
para verificar se o upload terminou, assim que ele é finalizado outro é iniciado logo em seguida e a cada arquivo upado é informado em um log para que as atualizações possam ser acompanhadas.

As bibliotecas utilizadas nesse projeto foram:

Time, Os, Pyautogui, Datetime, Logging e Selenium
