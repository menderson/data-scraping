import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import json

titles = []
prices = []
    
pages = ['1','2']
for page in pages:
    url = 'https://loja.asus.com.br/ofertas?p=' + page

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    lista_produtos = soup.find_all('div',class_='regular')

    for lista_titulos in lista_produtos:
        lista = lista_titulos.find_all('div', class_='product-info')
        
        for lista_dados in lista:
            titulo = lista_dados.find('a', class_='product-name').get('title')
            valor = lista_dados.find('p', class_='special-price').find('span', class_='price')
            
            if(valor.find('span', class_='price') != None): #há dois tipos de estruturas para representar o valor
                valor = valor.find('span', class_='price').next_element
            else:
                valor = valor.next_element.split(' ')[-1]
                valor = valor.split('\t')[0]
            prices.append(valor)
            titles.append(titulo)
    
df = pd.DataFrame({'price': prices, 'title': titles})

df.to_string('products.txt')
df.to_csv('products.csv')
df.to_json('productsGroupPricesTitles.json')

items = df.to_dict('items')

js = json.dumps(items)
fp = open('productsGroupItems.json', 'w')
fp.write(js)
fp.close()
