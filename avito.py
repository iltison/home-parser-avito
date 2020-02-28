from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np
link = 'https://www.avito.ru/asha/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&p=4'


class avito_parser():
    def get_html(self, link):
        response = requests.get(link)
        return response

    def parse_link(self,response):
        tree = BeautifulSoup(response.content, 'html.parser')
        return tree

    def get_pages(self,soup):
        pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')[-2].text
        return int(pages)
    
    def processing_data(self,tree,pages):
        all_tittle = []
        all_prices = []
        all_adress = []

        for p in range(pages):
            tittle = tree.find_all('a', {'class' : 'snippet-link'})
            for tl in tittle:
                all_tittle.append(tl.text)
            prices = tree.find_all('span', {'class' : 'snippet-price'}) 
            for pr in prices:
                all_prices.append(pr.text)
            adress = tree.find_all('span', {'class' : 'item-address__string'}) 
            for adr in adress:
                all_adress.append(adr.text)
        data = { 
        'name': all_tittle,
        'price': all_prices,
        'adress': all_adress
        }
        return data

    def save_data(self,data):
        df = pd.DataFrame(data = data)
        df.to_csv('s.csv')

    def run(self):
        response = self.get_html(link)
        tree = self.parse_link(response)
        pages = self.get_pages(tree)

        data = self.processing_data(tree,pages)
        self.save_data(data)

if __name__ == '__main__':
    avito_parser().run()

