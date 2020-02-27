from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np
link = ''


class avito_parser():
    def get_total_link(self):
        pass
    def get_link(self):
        pass
    
    def parse_link(self):
        response = requests.get(link)
        tree = BeautifulSoup(response.content, 'html.parser')
        return tree
        
    def processing_data(self,tree):
        
        tittle = tree.find_all('a', {'class' : 'snippet-link'})
        tittle = [tl.text for tl in tittle]

        prices = tree.find_all('span', {'class' : 'snippet-price'}) 
        prices = [pr.text for pr in prices]

        adress = tree.find_all('span', {'class' : 'item-address__string'}) 
        adress = [adr.text for adr in adress]
        array = [tittle,prices,adress]
        return array

    def save_data(self,array):
        dic_data = { 'name': array[0],
        'price': array[1],
        'adress': array[2]
        }
        df = pd.DataFrame(data = dic_data)
        df.to_csv('s.csv')

    def run(self):
        tree = self.parse_link()
        array = self.processing_data(tree)
        self.save_data(array)

if __name__ == '__main__':
    avito_parser().run()

