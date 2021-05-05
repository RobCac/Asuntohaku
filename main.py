import pandas as pd
import numpy as np
import data_scraper
import dataframe_cleaner
import Reittiopas_integration as ri 


try:
    df_apart = pd.read_csv('dataactual.csv', dtype= {'Postinmr':str})
except:    
    df_apart = data_scraper.etuovi_get_apartments() #dataactual.csv



try:
    df_hintakeh = pd.read_csv('Area_data.csv', dtype= {'Postinmr':str})
except:
    print("No existing Area_data.csv. Creating new one.")
    df_hintakeh = data_scraper.hintakehitys_scraper() #Area_data.csv

try:
    df_apart = pd.read_csv('data_clean.csv', dtype= {'Postinmr':str})
except:
    df_apart = dataframe_cleaner.data_clean_etu(df_apart)
#df = pd.read_csv('dataactual.csv', dtype= {'Postinmr':str})

df_combined = pd.merge(df_apart, df_hintakeh, on="Postinmr")

df_with_journeys = ri.add_journeys_to_df(df_combined)
df_with_journeys.to_csv('data_with_journeys.csv', header=True, index = False)
#In [11]: result = pd.concat([df1, df4], axis=1).reindex(df1.index)