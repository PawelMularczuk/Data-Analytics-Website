import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib
import base64


# Importuję plik i wybieram odpowiedni akrusz
table = pd.read_excel('./2015_2050_prognoza_rezydentow.xls', sheet_name='pięcioletnie grupy wieku')

# Usuwam wszystkie dane z wartościami NaN
table.dropna(inplace=True)

# Sprawdzam nazwy kolumn żemy je zmodyfikować
table.columns

# Za pomocą listy zmieniam nazwy kolumn
table.columns = ['Rok', 'Wiek', 'Ogółem', 'Mężczyźni','Kobiety']

# Usuwam niepotrzebne wartośći wskazując na index
table.drop(index=1, inplace=True)


# Teraz ustalam co ma być indexem 
table.set_index('Rok', inplace=True)


table.drop(columns='Wiek',inplace=True)

commonalty = table.copy() 


commonalty = commonalty['Ogółem']
commonalty1 = commonalty.copy()

# sns.set(style = 'whitegrid')

# plt.ticklabel_format(axis='y', style='plain')
# commonalty.plot(figsize=(15,10), xticks=(range(0,37,2)), ylabel='Ogółem')


natural_movement = pd.read_excel('./2015_2050_prognoza_rezydentow.xls', sheet_name='ruch naturalny i wędrówkowy')

natural_movement.drop(index=[0,1,2], inplace=True)

natural_movement.drop(columns=['Unnamed: 1','Unnamed: 6'], inplace=True)

natural_movement.columns = ['Rok', 'Urodzenia', 'Zgony', 'Imigracja', 'Emigracja']

natural_movement.set_index('Rok', inplace=True)

data = {'Urodzenia': [natural_movement['Urodzenia'].sum()],
        'Zgony' : [natural_movement["Zgony"].sum()]}

produce_death = pd.DataFrame(data, index=['Suma lat 2014-2050'])




deathx = pd.DataFrame(natural_movement['Zgony'])


natural_movement1 = pd.read_excel('./2015_2050_prognoza_rezydentow.xls', sheet_name='ruch naturalny i wędrówkowy')

natural_movement1.drop(index=[0,1,2], inplace=True)

natural_movement1.drop(columns=['Unnamed: 1','Unnamed: 6'], inplace=True)

natural_movement1.columns = ['Rok', 'Urodzenia', 'Zgony', 'Imigracja', 'Emigracja']


# xd = natural_movement1.columns = ['Rok','Urodzenia']

# print(xd)

# death = pd.DataFrame(xd)

columnsx = {'Rok' : natural_movement1['Rok'],
            'Zgony' : natural_movement1['Zgony']}


death = pd.DataFrame(columnsx)


columnss = {'Rok' : natural_movement1['Rok'],
           'Urodzenia' : natural_movement1['Urodzenia']}

produce = pd.DataFrame(columnss)






# importuje plik xls oraz odpowiendi arkusz
sex = pd.read_excel('./2015_2050_prognoza_rezydentow.xls', sheet_name='roczniki')

sex.columns=['Rok','Wiek','Ogółem','Mężczuźni','Kobiety']

sex.drop(index=[0,1], inplace=True)

sex['Rok'].fillna(method='pad', inplace=True)

value = sex.query("Wiek in ['25','26','27','28','29','30','31','32','33','34','35']")

value.set_index('Rok', inplace=True)

xd = pd.DataFrame(value['Kobiety'])

xd.loc[2015].sum()

year = []
list = []
for x in range(2014,2050+1):
    list.append(xd.loc[x].sum())
    year.append(x)

women = pd.DataFrame(list, index=year)    

women.columns = ['Kobiety w wieku 25-35']

women





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

# age2014 = okej_['Rok'] == '2014'

# age2014 = okej_[age2014]

# age2014.set_index('Wiek', inplace=True)

# # age2014 = age2014.drop(columns='Rok')

# age2014


age2030 = okej_['Rok'] == '2030'

age2030 = okej_[age2030]

age2030.set_index('Wiek', inplace=True)

# age2030.drop(columns='Rok')

age2030



age2040 = okej_['Rok'] == '2040'

age2040 = okej_[age2040]

age2040.set_index('Wiek', inplace=True)

# age2040.drop(columns='Rok', inplace=True)

age2040



age2050 = okej_['Rok'] == '2050'

age2050 = okej_[age2050]

age2050.set_index('Wiek', inplace=True)

# age2050.drop(columns='Rok', inplace=True)

age2050


age2014 = okej_['Rok'] == '2014'

age2014 = okej_[age2014]

age2014.set_index('Wiek', inplace=True)

# age2014 = age2014.drop(columns='Rok')

age2014


plt.pie(age2030['Ogółem'],labels=age2030.index, autopct='%1.2f%%')
plt.subplot()

img=io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plot_data6 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))