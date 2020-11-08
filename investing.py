import investpy as inv
from datetime import date
import pandas as pd
import scipy.cluster.hierarchy as shc
import scipy
import numpy as np
from pypfopt.hierarchical_portfolio import HRPOpt
import json
import matplotlib.pyplot as plt
import os
import seaborn as sns

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

    (1 + returns).cumprod().plot()
    plt.plot()
    plt.savefig('returns.png')

    returns.columns = ['Darius:', 'Axis:', 'Arx:', 'BCFF11:', 'IVVB11:']

    last_returns = returns.iloc[-1] * 100
    last_vols = returns.std() * np.sqrt(252/window)

    report = 'Retornos: \n' + last_returns.to_string() + '\n\n'
    report += 'Volatilidades: \n' +  last_vols.to_string() + '\n'
    report += 'Última data disponível: ' + get_last_date_available(returns)

    return report

def plot_clustermap(returns):

    sns.color_palette('viridis', as_cmap=True)

    cg = sns.clustermap(returns.cov(), method='ward', metric='euclidean', xticklabels=returns.columns, yticklabels=returns.columns, cmap='viridis')

    cg.savefig('clustermap.png')

def optimize_portfolio(riskless_index = 2, risk_threshold = 0.5):

    returns = get_investiments_returns()
    plot_clustermap(returns)

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

def risk_riskless_period_return(returns_port, date, riskless_index = 2, risk_threshold = 0.5):

    returns = returns_port.iloc[:date]
    
    riskless_returns = returns.iloc[:, :riskless_index ]
    risk_returns = returns.iloc[:, riskless_index: ]

    opt_riskless = HRPOpt(riskless_returns, riskless_returns.cov())
    weights_riskless = np.array(list(opt_riskless.optimize('ward').values())) * (1 - risk_threshold)

    opt_risk = HRPOpt(risk_returns, risk_returns.cov())
    weights_risk = np.array(list(opt_risk.optimize('ward').values())) * risk_threshold

    portfolio_weights = np.array([*weights_riskless, *weights_risk])

    last_period_returns = np.dot(portfolio_weights, returns_port.iloc[date])

    return last_period_returns

def make_rents_image(cumulative_returns):
    cumulative_returns.plot()
    plt.title('Rentabilidade mensal')
    plt.show()
    plt.savefig('rents.png')

def make_rents_dist_image(returns_model):
    cg = sns.distplot(returns_model)
    plt.axvline(returns_model.mean()[0], 0, 10, color='red')
    plt.title('Distribuição dos retornos mensais')
    plt.show()
    cg.savefig('rents_dist.png')

def backtesting(risk_threshold = 0.5):
    """
    Função que realiza o backtesting do algoritmo
    """
    
    returns = get_investiments_returns(pct_change_window=20)
    returns_monthly = returns.resample('BM').last().ffill()

    start_date = 2
    end_date = len(returns_monthly) - 1

    returns_model = []  

    for time_step in range(start_date, end_date):
        
      returns_model.append(risk_riskless_period_return(returns_monthly, date=time_step, risk_threshold = risk_threshold))

    returns_model = pd.DataFrame(returns_model, columns=['Retornos'])

    returns_model.index = returns_monthly.iloc[start_date:end_date].index

    cumulative_returns = (1 + returns_model).cumprod()

    make_rents_image(cumulative_returns)

    make_rents_dist_image(returns_model)

    report = 'Rentabilidade: ' + str(cumulative_returns.iloc[-1][0]) + '\n'
    report += 'Volatilidade: ' + str(returns_model.std()[0] * np.sqrt(12)) + '\n'
    report += 'Sharpe Ratio: ' + str(((returns_model.mean() * 12 - 0.02) /( returns_model.std() * np.sqrt(12)))[0]) + '\n'
    report += 'Kolmogorov-Smirnov P-value: ' + str(scipy.stats.kstest(returns_model, 'norm')[1]) + '\n'
    report += 'Kurtosis: ' + str(scipy.stats.kurtosis(returns_model)[0]) + '\n'
    report += 'Skewness: ' + str(scipy.stats.skew(returns_model)[0]) + '\n'
    report += 'Probabilidade de lucro no ano: ' + str(1 - scipy.stats.norm(returns_model.mean() * 12 , returns_model.std() * np.sqrt(12)).cdf(0)[0])
        
    return report