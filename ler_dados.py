#Esse arquivo tem como objetivo a leitura dos dados de entrada do sistema e de geração e carga

import pandas as pd # Importação da biblioteca pandas para leitura dos dados

dados_anos=pd.read_csv("dados.txt") # Leitura dos dados de geração e carga de 1 ano
dados_semana=pd.read_csv("dados1semana.txt") # Leitura dos dados de geração e carga de 1 semana
dados_dia=pd.read_csv("dados1dia.txt") # Leitura dos dados de geração e carga de 1 dia
sistema = pd.read_csv('ieee33barras.csv', sep=";") #Leitura dos dados do sistema IEEE 33 barras