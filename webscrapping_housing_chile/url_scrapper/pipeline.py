from scrapper import scrapper_comunas, list_to_df
import pandas as pd

rent = True
appartment = True
if rent == True:
    concept = 'arriendo'
else:
    concept = 'venta'
if appartment == True:
    type = 'departamento'
else:
    type = 'casa'

appartment_list, list_comunas = scrapper_comunas(concept, type, comunas = ['maipu'])
df = list_to_df(appartment_list, list_comunas)
df['pub_id'] = df.url.apply(lambda x: int(x.split('-')[1]))
print(df.head())