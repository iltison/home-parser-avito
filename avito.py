from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np

from datetime import datetime, date
name_csv = str(datetime.today().date()) + '.csv'


from setting import link_home as link


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
        tittle = tree.find_all('a', {'class' : 'snippet-link'})
        area = [tl.text.split(' ')[1] for tl in tittle]
        territory = [tl.text.split(' ')[5] for tl in tittle]
        href = [tl.get('href') for tl in tittle]


        prices = tree.find_all('span', {'class' : 'snippet-price'}) 
        prices = [''.join(pr.text.split(' ')[1:-2]) for pr in prices]
        adress = tree.find_all('span', {'class' : 'item-address__string'}) 
        adress = [' '.join(adr.text.split(' ')[1:-1]) for adr in adress]

        data = { 
        'area': area,
        'territory': territory,
        'price': prices,
        'adress': adress,
        'href': href
        }

        return data

    def save_data(self,data):
        try:
            df = pd.read_csv('home/' + name_csv)
            df2 = pd.DataFrame(data = data)
            df3 = pd.concat([df, df2], ignore_index=True,sort=False)
            df3[['area','territory','price','adress','href']].to_csv('home/' + name_csv)
        except:
            df = pd.DataFrame(data = data)
            df.to_csv('home/' + name_csv)
        print(df.shape)

    def run(self):
        response = self.get_html(link)
        tree = self.parse_link(response)
        pages = self.get_pages(tree)

        for i in range(1,pages + 1):
            link_page = link + str(i)
            response = self.get_html(link_page)
            print(link_page)
            tree = self.parse_link(response)
            data = self.processing_data(tree,pages)
            self.save_data(data)
        

if __name__ == '__main__':
    avito_parser().run()

