import pandas as pd 
import numpy as np
# -*- coding: UTF-8 -*-
df = pd.read_csv('dataactual.csv', dtype= {'Postinmr':str})
df = df.reindex(columns = df.columns.tolist() + ['Kaupunki'])
#df['Pinta-ala'] = df['Pinta-ala'].apply(lambda x: x.str.replace(',','.'))
def data_clean_etu(df):
    #df['Postinmr'] = df['Postinmr'].astype(str)
    for i in range(len(df['Osoite'])):
        splitlist = df.loc[i,'Osoite'].split(',')
        df.loc[i,'Osoite'] = splitlist[0]
        df.loc[i, 'Kaupunki'] = splitlist[-1]
        splitlist = df.loc[i,'Pinta-ala'].split(' ')
        df.loc[i, 'Pinta-ala'] = float(splitlist[0])
        esa = df.loc[i, 'Vmh']
        df.loc[i, 'Vmh'] = int(esa[:3]+esa[4:7])
        splitlist = df.loc[i, 'URL'].split('?')
        df.loc[i, 'URL'] = splitlist[0]
        df.loc[i,'Postinmr'] = str(df.loc[i,'Postinmr'])
    df.to_csv('data_clean.csv', header=True)


data_clean_etu(df)