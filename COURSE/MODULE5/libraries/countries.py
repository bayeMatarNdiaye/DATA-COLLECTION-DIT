from .utils import Utils
from .bceao import CurrencyScrapper
from .bceao import URL
from .utils import Utils
import requests
import pandas as pd
import json


url = 'https://restcountries.com/v3.1/all'

class ApiFetcher(object):
    
    def httpFetcher(cls, url : str, params = None, headers = None):
        with requests.Session() as session : 
            res = session.get(url, params = params, headers= headers)
            return res.json()


    def countriesLister(cls, data):
        res = []
        for item in data:
            res.append(
                {
                    'name' : item['name']['official'],
                    'flag' : item['flags']['png']
                }
            )
        return res   


    @classmethod
    def addCountriesName(cls,  listCountries):
        print(Utils.divider())
        df1 = (CurrencyScrapper.main())
        df2 = CurrencyScrapper.makeCurrencyList(URL)
        newdf = Utils.contertToXOF(df1,df2)
        
        fetched = ApiFetcher.httpFetcher(cls, url)
        listCountries = ApiFetcher.countriesLister(cls, fetched)
        data = pd.DataFrame.from_dict(listCountries, orient='columns')
        dataCountries = data['name']
        
        newdf['country'] = ''
        newdf['country'] = newdf['country'].apply(lambda x: Utils.choiceRandomise(dataCountries))
        
        return newdf


    @classmethod
    def addCountriesFlag(cls, df1, df2):
        df1["flag"] = ""
        for i in range(len(df2)):
            for j in range(len(df1)):
                if df1['country'][j] == df2['name'][i]:
                    df1['flag'][j] = df2['flag'][i]
        return df1


    @classmethod
    def main(cls):

        data = ApiFetcher.httpFetcher(cls, url)
        data = ApiFetcher.countriesLister(cls, data)
        data = ApiFetcher.addCountriesName(data)
        fetched = ApiFetcher.httpFetcher(cls, url)
        listCountries = ApiFetcher.countriesLister(cls, fetched)
        dataCountries = pd.DataFrame.from_dict(listCountries, orient='columns')
        dataframe = ApiFetcher.addCountriesFlag(data, dataCountries)
        return dataframe