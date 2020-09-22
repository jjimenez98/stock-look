from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
yf.pdr_override()
import pandas as pd


class stock:
    def __init__(self,ticker,amount,date):
        self.ticker = ticker
        self.amount = amount
        self.prices = list()
        self.data = dict(open=0,high=0,low=0,close=0,adj_close=0)
        self.date = date

    def __repr__(self):
        return '<STOCK %r>' % self.ticker

    def getinfo(self):
        today = date.today()
        days = 0
        if self.date == 'week':
            days = 7
        if self.date == 'month':
            days = 30
        if self.date == '3month':
            days = 90
        if self.date == 'year':
            days = 365
        monthAgo = today - timedelta(days=days)
        data = pdr.get_data_yahoo(self.ticker, start=monthAgo, end=today,freq='B')
        df = pd.DataFrame(data)
        for index, row in df.iterrows():
            self.prices.append(row['Close'])
        self.data['open'] = df.tail(1)['Open'][0]
        self.data['high'] = df.tail(1)['High'][0]
        self.data['low'] = df.tail(1)['Low'][0]
        self.data['close'] = df.tail(1)['Close'][0]
        self.data['adj_close'] = df.tail(1)['Adj Close'][0]

        




