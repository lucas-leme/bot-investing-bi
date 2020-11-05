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

    stocks_name = ['bcff11']
    funds_name = ['Visia Zarathustra Fundo De Investimento Em Cotas De Fundo De Investimento Multimercado',
                  'Visia Axis Fundo De Investimento Em Cotas De Fundos De Investimento Multimercado',
                  'Arx Fundo De Investimento Em Ações',]
    etfs_name = ['Fundo de Invest Ishares SP 500']


    today = date.today()
    today = today.strftime("%d/%m/%Y")    

    close_prices = []
    for fund in funds_name:
        prices = inv.get_fund_historical_data(fund, country='brazil', from_date='01/01/2015', to_date=today)
        close_prices.append(prices.Close)

    for stock in stocks_name:
        prices = inv.get_stock_historical_data(stock=stock, country='brazil', from_date='01/01/2015', to_date=today)
        close_prices.append(prices.Close)

    for etf in etfs_name:
        prices = inv.get_etf_historical_data('Fundo de Invest Ishares SP 500', country='brazil', from_date='01/01/2015', to_date=today)
        close_prices.append(prices.Close)

    prices = pd.concat(close_prices, axis=1)
    prices = prices.dropna()

    prices.columns = ['Darius', 'Axis', 'Arx', 'BCFF11', 'IVVB11']

    returns = prices.pct_change(pct_change_window).dropna()

    # Zara -> Darius conversion
    returns.Darius *= 2/3

    return returns

def get_last_date_available(returns):
  
  last_date = str(returns.index[-1])[:10]

  return last_date

def get_investiments_last_period_performace(window = 1):

    returns = get_investiments_returns(window)

    returns.plot()
    plt.plot()
    plt.savefig('image.png')

    returns.columns = ['Darius:', 'Axis:', 'Arx:', 'BCFF11:', 'IVVB11:']

    last_returns = returns.iloc[-1] * 100
    last_vols = returns.std() * np.sqrt(252/window)

    report = 'Retornos: \n' + last_returns.to_string() + '\n\n'
    report += 'Volatilidades: \n' +  last_vols.to_string() + '\n'
    report += 'Última data disponível: ' + get_last_date_available(returns)

    return report


def optimize_portfolio(riskless_index = 2, risk_threshold = 0.5):

    returns = get_investiments_returns()

    riskless_returns = returns.iloc[:, :riskless_index ]
    risk_returns = returns.iloc[:, riskless_index: ]

    opt_riskless = HRPOpt(riskless_returns, riskless_returns.cov())
    weights_riskless = np.array(list(opt_riskless.optimize('ward').values())) * (1 - risk_threshold)

    opt_risk = HRPOpt(risk_returns, risk_returns.cov())
    weights_risk = np.array(list(opt_risk.optimize('ward').values())) * risk_threshold

    portfolio_weights = np.array([*weights_riskless, *weights_risk])

    expected_return = np.dot(portfolio_weights, returns.mean()) * 252
    annual_vol = np.sqrt(np.dot(portfolio_weights.T, np.dot(returns.cov(), portfolio_weights))) * np.sqrt(252)
    sharpe_ratio = (expected_return - 0.02) / annual_vol

    performace_formated = 'Retorno esperado: ' + str(expected_return) + '\n' + 'Volatilidade Anual: ' + str(annual_vol) + '\n' + 'Sharpe Ratio: ' + str(sharpe_ratio)

    portfolio_weights_formated = json.dumps(dict(zip(returns.columns, portfolio_weights)))[1:-1].replace(',', '\n')

    return (portfolio_weights_formated, performace_formated)