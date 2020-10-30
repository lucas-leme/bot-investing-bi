import investpy as inv
from datetime import date
import pandas as pd
import scipy.cluster.hierarchy as shc
import numpy as np
from pypfopt.hierarchical_portfolio import HRPOpt
import json
import matplotlib.pyplot as plt
import os

def get_assets_env_var(env_var):
    assets = os.environ.get(env_var).split('; ')

    return assets

def get_investiments_returns(pct_change_window=1):

    stocks_name = get_assets_env_var('STOCKS')
    funds_name = get_assets_env_var('FUNDS')


    today = date.today()
    today = today.strftime("%d/%m/%Y")    

    close_prices = []
    for stock in stocks_name:
        prices = inv.get_stock_historical_data(stock=stock, country='brazil', from_date='01/01/2015', to_date=today)
        close_prices.append(prices.Close)

    for fund in funds_name:
        prices = inv.get_fund_historical_data(fund, country='brazil', from_date='01/01/2015', to_date=today)
        close_prices.append(prices.Close)

    prices = pd.concat(close_prices, axis=1)
    prices = prices.dropna()

    columns_name = stocks_name + funds_name
    for column_name in columns_name:
        column_name[:10]

    prices.columns = columns_name

    returns = prices.pct_change(pct_change_window).dropna()

    return returns

def get_last_date_available(returns):
  
  last_date = str(returns.index[-1])[:10]

  return last_date

def get_investiments_last_period_performace(window = 1):

    returns = get_investiments_returns(window)

    last_returns = returns.iloc[-window] * 100

    report = 'Valores percentuais: \n' + last_returns.to_string() + '\n'
    report = report + 'Última data disponível: ' + get_last_date_available(returns)


    # returns.plot()

    # image_path = 'plt.png'
    # plt.savefig(image_path)

    return report


def optimize_portfolio():

    returns = get_investiments_returns()
    cov_matrix = returns.cov()

    opt = HRPOpt(returns, cov_matrix)
    weights = opt.optimize('ward')

    weights = json.dumps(weights)[1:-1].replace(',', '\n')

    performace = opt.portfolio_performance()

    expected_return = performace[0]
    annual_vol = performace[1]
    sharpe_ratio = performace[2]

    performace_formated = 'Retorno esperado: ' + str(expected_return) + '\n' + 'Volatilidade Anual: ' + str(annual_vol) + '\n' + 'Sharpe Ratio: ' + str(sharpe_ratio)

    return (weights, performace_formated)