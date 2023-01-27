from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time


def try_get_pub_date(soup, info_dict):
    """Try to get the publication date of the real state.
    Args:
        soup: str
        info_dict: dict
    
    Returns:
        Dictionary: Dictionary with information regarding the publication date.
    """
    try:
        pub_date = soup.find_all('p', attrs = {'class': 'ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle'})[0].text.split(' ')
        info_dict['pub_date'] = [pub_date[2]]
        info_dict['pub_date_unit'] = [pub_date[3]]    
    except Exception:
        try:
            pub_date = soup.find_all('p', attrs = {'class': 'ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title'})[0].text.split(' ')
            info_dict['pub_date'] = [pub_date[2]]
            info_dict['pub_date_unit'] = [pub_date[3]]
        except:
            info_dict['pub_date'] = None
            info_dict['pub_date_unit'] = None
            
    return info_dict
            
def try_get_price(soup, info_dict):
    """Try to get price of the real state.
    Args:
        soup: str
        info_dict: dict
    
    Returns:
        Dictionary: Dictionary with information regarding the price.
    """
    try:  
        price = int(soup.find_all('span', attrs = {'class': 'andes-money-amount__fraction'})[0].text.replace('.', ''))
        info_dict['price_clp'] = [price]
    except:
        info_dict['price_clp'] = None
        
    return info_dict
        
def try_get_characteristics(soup, info_dict):
    """Try to get characteristics of the real state.
    Args:
        soup: str
        info_dict: dict
    
    Returns:
        Dictionary: Dictionary with information regarding characteristics of the house.
    """
    try:
        table = soup.find_all('tbody', attrs = {'class': 'andes-table__body'})
        table_row = table[0].find_all('tr', attrs = {'class': 'andes-table__row'})
        for row in range(len(table_row)):
            attribute = table_row[row].find_all('th', attrs = {'class': 'andes-table__header andes-table__header--left ui-pdp-specs__table__column ui-pdp-specs__table__column-title'})[0].text
            value = table_row[row].find_all('span', attrs = {'class': 'andes-table__column--value'})[0].text
            info_dict[attribute] = [value]
        success = True
    except:
        print('Table not found')
        success = False
    
    return info_dict, success
                
def try_get_location(soup, info_dict):
    """Try to get the location of the real state.
    Args:
        soup: str
        info_dict: dict
    
    Returns:
        Dictionary: Dictionary with information regarding location of the house.
    """
    try:
        location_set = soup.find_all('div', attrs = {'class': 'ui-pdp-media__body'})

        for item in location_set:
            if 'Ver información de la zona' in item.text:
                location = item.text.split(',')
                
        len_loc = len(location)
        address = location[0].lstrip()
        comuna = location[len_loc-2].lstrip()
        region = location[len_loc-1][:-26].lstrip()
        
        info_dict['address'] = [address]
        info_dict['comuna'] = [comuna]
        info_dict['region'] = [region]

    except:
        print('Location not found')
        info_dict['address'] = None
        info_dict['comuna'] = None
        info_dict['region'] = None
    
    return info_dict

def features_scrapper(df_scrap, df_url):
    """Given a DataFrame with urls to scrappe and
    a DataFrame to tag a scrapped url, iterate over them and scrappe.
    Args:
        df_scrap: pd.DataFrame
        df_url: pd.DataFrame
    
    Returns:
        pd.DataFrame: Two DataFrames, one for features and the other one for scrapping tag
    """

    urls_deptos = df_scrap.url.to_list()
    apartment_info_lst = []
    for url in urls_deptos:   
        try:
            time.sleep(7)
            html = urlopen(url)
            soup = BeautifulSoup(html, "html.parser")
        except:
            print(url)
            continue    
        info_dict = {}
        info_dict['url'] = [url]
        info_dict['comuna_url'] = df_scrap[df_scrap['url'] == url].comuna

        info_dict, success = try_get_characteristics(soup, info_dict)
        if success:
            info_dict = try_get_pub_date(soup, info_dict)
            info_dict = try_get_price(soup, info_dict)
            info_dict = try_get_location(soup, info_dict)
            #df_url.loc[df_url.url == url, 'got_scrapped'] = True
        else:
            #df_url.loc[df_url.url == url, 'got_scrapped'] = False
            continue
        
        apartment_info = pd.DataFrame.from_dict(info_dict)
        apartment_info_lst.append(apartment_info)

    df = pd.concat(apartment_info_lst)
    df['partition_date'] = pd.to_datetime("today").strftime ("%Y-%m-%d")

    return df, df_url