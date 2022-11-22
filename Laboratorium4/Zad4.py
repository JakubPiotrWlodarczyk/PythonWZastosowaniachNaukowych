import requests
from bs4 import BeautifulSoup
import argparse
import json
import tqdm

parser = argparse.ArgumentParser()  #argumenty

parser.add_argument('-json', '--nazwa_pliku_json', default = 'plik_json')

args = parser.parse_args()
plik = args.nazwa_pliku_json    #argument wejsciowy

list_of_products = []

req = requests.get('https://www.olx.pl/d/oferty/q-gry-xbox360/?search%5Bfilter_float_price:from%5D=1&view=list')    #wywolanie strony

if(req.status_code==200):  #status polaczenia
    print('Polaczono poprawnie')

    soup = BeautifulSoup(req.text, 'html.parser') #parsowanie strony przez soup

    tools = soup.find('div', {'class': 'listing-grid-container css-d4ctjd'}) #nazwa elementu, slownik 

    for tool in tools.find_all('div', {'data-cy': 'l-card'}):
        #step = tool.find('a', {'class': 'css-rc5s2u'})
        #step2 = step.find('div', {'class': 'css-qfzx1y'})
        #step3 = step2.find('div', {'class': 'css-1venxj6'})
        #step4 = step3.find('div', {'class': 'css-1apmciz'})
        #step5 = step4.find('div', {'class': 'css-u2ayx9'})

        step5 = tool.find('div', {'class': 'css-u2ayx9'})

        prod = step5.find('h6')
        product = str(prod.text.strip())
        
        pric = step5.find('p')  
        price = str(pric.text.strip())

        list_of_products.append((product, price))   #dodaje do listy tupla z produktem i cena


    with open(str(plik)+'.json','w', encoding="utf8") as f:     #otwieram i zapisuje
        json.dump(list_of_products, f, ensure_ascii=False, indent=4)

else:
    print('Blad polaczenia!')