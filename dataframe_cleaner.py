import pandas as pd 
import numpy as np
# -*- coding: UTF-8 -*-
df = pd.read_csv('data.csv')
df = df.reindex(columns = df.columns.tolist() + ['Kaupunki', 'Postinmr'])
#df['Pinta-ala'] = df['Pinta-ala'].apply(lambda x: x.str.replace(',','.'))
def data_clean_etu(df, columns = ['Osoite, Vmh', 'Pinta-ala', 'URL']):
    for i in range(len(df['Osoite'])):
        splitlist = df.loc[i,'Osoite'].split(',')
        df.loc[i,'Osoite'] = splitlist[0]
        df.loc[i, 'Kaupunki'] = splitlist[-1]
        splitlist = df.loc[i,'Pinta-ala'].split(' ')
        df.loc[i, 'Pinta-ala'] = float(splitlist[0])
        esa = df.loc[i, 'Vmh']
        df.loc[i, 'Vmh'] = int(esa[:3]+esa[4:7])
        
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


data_clean_etu(df)