import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np


def average_price_eval(df, house = all):
    house_square_price = list()
    avg_square_price = list()
    address = list()
    for i in range(len(df['Osoite'])):
        address.append(df.loc[i, 'Osoite'])
        house_square_price.append(round(float(df.loc[i, 'Vmh']) / float(df.loc[i, 'Pinta-ala']), 1))
        avg_square_price.append(df.loc[i, 'Keskineliöhinta'])
    x = np.arange(len(address))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x-width/2, house_square_price, width, label = 'Neliöhinta')
    rects2 = ax.bar(x+width/2, avg_square_price, width, label = 'Alueen neliöhinta')

    ax.set_ylabel("Hinnat euroissa")
    ax.set_title('Neliöhintavertailu')
    ax.set_xticks(x)
    ax.set_xticklabels(address)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.setp(ax.get_xticklabels(), rotation = 30, horizontalalignment= 'right')

    fig.tight_layout()

    plt.show()


try:
    df = pd.read_csv('data_with_journeys.csv', dtype= {'Postinmr':str})
except:    
    print("Hups")
average_price_eval(df)