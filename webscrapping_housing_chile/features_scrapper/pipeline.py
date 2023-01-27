from scrapper import features_scrapper
import pandas as pd
import os

# Here you can test the pipeline given some url samples

path = os.getcwd()
print(path)
print('HOLAAAAA')

test_url_list = ['https://www.portalinmobiliario.com/MLC-1283852355-venta-de-5-propiedades-de-379-en-426-metros-cuadrados-_JM#position=1&search_layout=stack&type=item&tracking_id=3461dfc9-c0d9-4921-8dc8-defb4eb82c12',
                 'https://www.portalinmobiliario.com/MLC-1283852590-casa-en-venta-de-15-dormitorios-en-santiago-_JM#position=2&search_layout=stack&type=item&tracking_id=3461dfc9-c0d9-4921-8dc8-defb4eb82c12',
                 'https://www.portalinmobiliario.com/MLC-1283503038-casa-victoriasantiaguillo-_JM#position=3&search_layout=stack&type=item&tracking_id=3461dfc9-c0d9-4921-8dc8-defb4eb82c12',
                 'https://www.portalinmobiliario.com/MLC-1283859554-casa-club-hipicoantofagasta-_JM#position=4&search_layout=stack&type=item&tracking_id=3461dfc9-c0d9-4921-8dc8-defb4eb82c12',]
df_scrap = pd.DataFrame(test_url_list, columns=['url'])
df_scrap['comuna'] = 'santiago'
df, empty = features_scrapper(df_scrap, pd.DataFrame())
print(df.head())