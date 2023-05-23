Esse é um projeto de BI feito completamente em Python.

O intuito desse projeto é realizar a coleta todos os dados das ligações que foram realizadas de um discador no dia, realizar o tratamento desses dados deixando apenas o que é importante e formatado da forma necessária,
esses dados são inseridos em um banco de dados pelo proprio código. Cada dado é inserido em sua tabela correspondente para que eles possam ser puxados no Power BI e analisados, após toda a inserção dos dados
é gerado um log onde e informado todas as informações que não foram inseridas e qual foi o motivo da falha na inserção caso ocorra, também é enviado uma mensagem no telegram para informar que todo o código foi executado com sucesso.

As bibliotecas utilizadas nesse projeto foram:

Pyautogui, Pandas, MySql Connector, Numpy, Loggin, Datetime, TQDM, Selenium
