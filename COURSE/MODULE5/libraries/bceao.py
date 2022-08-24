from .utils import Utils
from .csv import CsvFactory
from .json import JsonFactory
from .html import HtmlFactory
import pandas as pd
import requests
from bs4 import BeautifulSoup

PATH_URL = 'cours/cours-des-devises-contre-Franc-CFA-appliquer-aux-transferts'
URL = f'https://www.bceao.int/fr/{PATH_URL}'


class DataSouper(object):
    @classmethod
    def httpFetcher(cls, URL):
        with requests.Session() as session:
            result = session.get(URL)
            result = result.text
            return result

class CurrencyScrapper(object):
    @classmethod
    def scrapLink(cls, URL):
        return DataSouper \
            .httpFetcher(URL)

    @classmethod
    def souper(cls, URL):
        result = cls.scrapLink(URL)
        return BeautifulSoup(
            result,
            'html.parser')

    @classmethod
    def getBoxCourse(cls, URL):
        soupering = cls.souper(URL)
        soupering = soupering \
            .find_all(attrs={
                'id': 'box_cours'})
        if soupering:
            table = soupering[0].table
            return table
        return None

    @classmethod
    def makeCurrencyList(cls, URL):
        soupering = cls.getBoxCourse(URL)
        if soupering:
            tr = soupering.find_all('tr')
            factory = [
                item.find_all('td')
                for item in tr
            ][1:]
            factory = [
                {
                    'Devise': x.string.strip(),
                    'Achat': float(y.string.strip().replace(',', '.')),
                    'Vente': float(z.string.strip().replace(',', '.')),
                }
                for (x, y, z) in factory
            ]
            factory = pd.DataFrame.from_dict(factory, orient='columns')
            return factory
        return None

    @classmethod
    def save(cls, URL, format=None):
        soupering = cls.makeCurrencyList(URL)
        if soupering:
            return soupering
        return None


    @classmethod
    def addDevise(cls, data):
        
        dataCsv = CsvFactory.main()
        dataJson = JsonFactory.main()
        dataHtml = HtmlFactory.main()
        globData =  dataCsv + dataJson + dataHtml
        data = pd.DataFrame.from_dict(globData, orient='columns')
        
        devList = ["Euro", "Dollar us", "Yen japonais"]
        data['devise'] = '' 
        data['devise'] = data['devise'].apply(lambda x: Utils.deviseRandomise(devList))
        return data


    


    @classmethod
    def main(cls):
        data = CurrencyScrapper.makeCurrencyList(URL)
        data = CurrencyScrapper.addDevise(data)
        return data

