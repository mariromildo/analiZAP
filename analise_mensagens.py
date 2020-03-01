# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import numpy as np
import pandas as pd
import os
#import re

# Leitura dos dados
caminho = 'C:/Users/HP/Downloads/Projetos/analizap'
os.chdir(caminho)

#dados = open('mensagens.txt', encoding = 'utf8')
dados = open('grupo_de_casa.txt', encoding = 'utf8')
dados = dados.read()

# Manipulação e tratamento do banco 
dados = pd.DataFrame([x.split(' - ', 1) for x in dados.split('\n')])
dados.columns = ['Data','Mensagem']

# Lidando com as mensagens de mais de uma linha
for i in np.arange(1,dados.shape[0]):
    if dados.Data[i].count("/") < 2:
        dados.Mensagem[i-1] = str(dados.Mensagem[i-1]) + " " + dados.Data[i]

# Criação das colunas
dados[['Data','Hora']] = dados.Data.str.split(' ',1,expand=True)
dados[['Autor','Mensagem']] = dados.Mensagem.str.split(': ',1,expand = True)

# Remoção da primeira linha e linhas com NA (ex linhas múltiplas)
dados = dados.dropna()

# Visão geral 
print(dados.describe())

# Quem enviou mais mensagens
autor_mais_mensagens = dados.Autor.value_counts()
autor_mais_mensagens = autor_mais_mensagens.sort_values(ascending = True) 
autor_mais_mensagens.plot.barh()

# Em que dia foram enviadas mais mensagens
data_mais_mensagens = dados.Data.value_counts()
data_mais_mensagens = data_mais_mensagens.sort_values(ascending = True)
data_mais_mensagens.plot.barh()

# Quantas figurinhas foram enviada (STK identifica)
dados['Figurinha'] = dados.Mensagem.str.contains('STK-')
dados.Figurinha.value_counts()

# Quem enviou mais figurinhas? 
contagem_figurinhas = dados.groupby('Autor')['Figurinha'].value_counts().unstack()

# Quantas fotos foram enviadas (IMG- identifica uma imagem)
dados['Imagem'] = dados.Mensagem.str.contains('IMG-')
dados.Imagem.value_counts()

# Quem enviou mais imagens? 
contagem_imagens = dados.groupby('Autor')['Imagem'].value_counts().unstack()

# Média de Anexos por dia
dados.groupby('Data').mean()

# Média de mensagens por dia
data_mais_mensagens.mean()

# Média de mensagens por autor
media_autor = dados.groupby('Data')['Autor'].value_counts().unstack()
media_autor.mean()

# Palavras por mensagem\
dados['Palavras'] = ''
for j in np.arange(0,len(dados)):
    if dados.Figurinha.iloc[j] == False and dados.Imagem.iloc[j] == False:
        dados.Palavras.iloc[j] = len(dados.Mensagem.iloc[j].split())
 #   else:
 #       dados.Palavras.iloc[j] = 'NaN'
             
palavras_mensagem = dados.groupby('Data').mean()