import random
from libraries.countries import ApiFetcher
from libraries.bceao import URL
from libraries.countries import url
from libraries.utils import Utils
from libraries.csv import CsvFactory
from libraries.json import JsonFactory
from libraries.html import HtmlFactory
from libraries.bceao import CurrencyScrapper
import pandas as pd


def toDataFrame():
    dataCsv = CsvFactory.main()
    dataJson = JsonFactory.main()
    dataHtml = HtmlFactory.main()
    globData =  dataCsv + dataJson + dataHtml
    data = pd.DataFrame.from_dict(globData, orient='columns')
    return data

if __name__ == '__main__' :
    print(Utils.divider())
    print(JsonFactory.main())
    print('\n')
    print(Utils.divider())
    print(CsvFactory.main())
    print('\n')
    print(Utils.divider())
    print(HtmlFactory.main())
    mydf = toDataFrame()
    print('\n\nGLOBAL DATA\n\n')
    print(mydf)
    print(Utils.divider())
    df1 = (CurrencyScrapper.main())
    df2 = CurrencyScrapper.makeCurrencyList(URL)
    print(df1)
    print(df2)
    newdf = Utils.contertToXOF(df1,df2)
    print(newdf)
    print(Utils.divider())
    print(ApiFetcher.main())    
    
