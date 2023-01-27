import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import random 


def open_url_bs4(url):
        html = urlopen(url)
        return BeautifulSoup(html, 'html.parser')

def scrap_subpages_number(soup):
    return int(soup.find_all('li', attrs = {'class': 'andes-pagination__page-count'})[0].text.split(' ')[1])

def generate_subpages_comuna(num_subpages, concept, type, comuna):
    """Given a number of subpages, generate the urls
    that correspond to a given comuna storing them in a list.
    Go until 8 subpages or max.
    
    Args:
        num_subpages: int
        concept: str
        type: str
        comuna: str
    
    Returns:
        List: List with generated urls.
    """
    url_page_deptos = []
    page = 0
    counter = 1
    if num_subpages >= 1:
        while (counter <= num_subpages-1):
            page+= 5
            counter += 1
            if counter == 8:
                break
            url_page_depto = f'https://www.portalinmobiliario.com/{concept}/{type}/{comuna}-metropolitana/_Desde_{page}1_NoIndex_True'
            url_page_deptos.append(url_page_depto)
    return url_page_deptos

def find_all_appartments(url):
        soup_apartment = open_url_bs4(url)
        return soup_apartment.find_all('div', attrs = {'class': 'ui-search-result__wrapper'})

def scrapper_comunas(
        concept, type, comunas: list = ['maipu', 'cerrillos']
                         ) -> pd.DataFrame:
    """For a list of comunas, find all appartment/houses
    urls there are in sell/rent in Portal Inmobiliario.
    
    Args:
        concept: str
        type: str
        comunas: list
    
    Returns:
        List: List of appartment urls with a list for the comuna.
    """
    appartment_list = []
    list_comunas = []
    for comuna in comunas:
        url_comuna = f'https://www.portalinmobiliario.com/{concept}/{type}/{comuna}-metropolitana'
        time.sleep(random.randint(1, 5))
        try:
            soup = open_url_bs4(url_comuna)
        except:
            print(f'Unable to find content for comuna {comuna}.')
            continue

        try:
            num_subpages = scrap_subpages_number(soup)
        except: 
            num_subpages = 0
            print(f'No subpages found for comuna {comuna}.')

        url_page_deptos = generate_subpages_comuna(num_subpages, concept, type, comuna)
        url_page_deptos.append(url_comuna) # Añadimos la pagina número 1

        for url in url_page_deptos:
            time.sleep(random.randint(1, 5))
            appartments_soup = find_all_appartments(url)
            for app in range(len(appartments_soup)):
                link_depto = appartments_soup[app].find_all('a', href=True)[0]['href']
                appartment_list.append(link_depto)
                list_comunas.append(comuna)
                
    return appartment_list, list_comunas

def list_to_df(appartment_list, list_comunas):
    """For two given lists, make a DataFrame
    
    Args:
        appartment_list: list
        list_comunas: list

    Returns:
        pd.DataFrame: DataFrame of appartment urls for comunas.
    """
    df_urls = pd.DataFrame(appartment_list, list_comunas, columns = ['url'])
    df_urls.reset_index(inplace=True)
    df_urls.rename(columns = {'index': 'comuna'}, inplace=True)
    return df_urls