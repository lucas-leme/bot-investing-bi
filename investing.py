import investpy as inv
from datetime import date
import pandas as pd

def get_investiments_returns(pct_change_window=1):

    stocks_name = ['bcff11', 'gogl34, aapl34']
    funds_name = ['Visia Zarathustra Fundo De Investimento Em Cotas De Fundo De Investimento Multimercado',
                  'Arx Fundo De Investimento Em Ações',
                  'Alaska Black Fundo De Investimento Em Cotas De Fundos De Investimento Em Ações Ii - Bdr Nível I',
                  'Constellation Fundo De Investimento Em Cotas De Fundos De Investimento De Ações']


    today = date.today()
    today = today.strftime("%d/%m/%Y")    

    close_prices = []
    for stock in stocks_name:
        prices = inv.get_stock_historical_data(stock=stock, country='brazil', from_date='01/01/2018', to_date=today)
        close_prices.append(prices.Close)

    for fund in funds_name:
        prices = inv.get_fund_historical_data(fund, country='brazil', from_date='01/01/2018', to_date=today)
        close_prices.append(prices.Close)
    
    asset_names = ['BCFF11', 'Google', 'Apple', 'Zarathustra', 'ARX', 'Alaska', 'Constellation']

    prices = pd.concat(close_prices, axis=1)
    prices = prices.dropna()
    prices.columns = assets_names 

    returns = prices.pct_change(pct_change_window).dropna()

    return returns

def get_investiments_last_period_performace(window = 1):

    returns = get_investiments_returns(window)

    last_returns = returns.iloc[-window] * 100

    return last_returns.to_string()