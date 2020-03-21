import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
import json

def main():

    today = date.today()

    tickers_list = ['NOK', 'ERIC']
    #data = pd.DataFrame(columns=tickers_list)
    data= yf.download(tickers_list,'2019-01-01',today)['Close']
    #print(data)
    #data.plot()
    #print(data.to_json(orient='table'))
    return json.loads(data.to_json(orient= 'table'))['data']


    #plt.show()
#print(nok.info)
#print(nok.history(period="1mo"))
#print(eric.history(period="year"))

#%matplotlib inline

if __name__== "__main__":
    main()
