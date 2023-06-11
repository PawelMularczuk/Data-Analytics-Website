import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import urllib
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Importuję plik i wybieram odpowiedni akrusz
date_ = pd.read_excel('./2015_2050_prognoza_rezydentow.xls', sheet_name='struktury pionowe')


date_.drop(columns=['Unnamed: 5', 'Unnamed: 6','Unnamed: 7','Unnamed: 8'], index=[0,1],inplace=True)

date_.columns=['Rok','Wiek','Ogółem','Mężczyźni','Kobiety']

date_.replace('przedprodukcyjny*','przedprodukcyjny', inplace=True)

date_['Rok'].fillna(method='pad', inplace=True)

value_ = date_.query("Wiek in ['przedprodukcyjny','mobilny','niemobilny','poprodukcyjny']")

okej_ = value_.copy()

okej_['Ogółem'] = pd.to_numeric(okej_['Ogółem'])

okej_.drop(columns=['Mężczyźni','Kobiety'],inplace=True)

age2014 = okej_['Rok'] == '2014'

age2014 = okej_[age2014]

age2014.set_index('Wiek', inplace=True)

# age2014 = age2014.drop(columns='Rok')


plt.pie(age2014['Ogółem'],  labels=age2014.index, autopct='%1.2f%%')
plt.subplot()

img=io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plot_data5 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))

    