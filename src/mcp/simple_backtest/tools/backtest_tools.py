#!/usr/bin/env python3

"""
tools/backtest_tools.py:
    1. backtest_portfolio: Runs portfolio backtest and returns time series
"""


from server import mcp
from utils.misc import (
    load_price_data,
    get_ticker_data,
    calculate_portfolio_returns,
    calculate_performance_metrics
)
from tools.data_tools import DEFAULT_CSV_PATH


@mcp.tool()
def backtest_portfolio(portfolio, price_data_path=DEFAULT_CSV_PATH) -> dict:
    """
        Backtest a portfolio given its weights and price data.
        
        Args:
            portfolio (dict): A dictionary where keys are tickers and values are weights.
            price_data_path (str): Path to the CSV file containing price data.
        
        Returns:
            dict: A dictionary containing portfolio returns and performance statistics.
    """
    raw_price_data = load_price_data(price_data_path)
    
    # Get tickers from portfolio
    tickers = list(portfolio.keys())
    
    # Get price data for portfolio tickers
    price_data = get_ticker_data(raw_price_data, tickers)
    
    # Calculate portfolio returns
    portfolio_returns = calculate_portfolio_returns(price_data, portfolio)
    
    # Calculate performance metrics
    performance_stats = calculate_performance_metrics(portfolio_returns)
    
    return {"portfolio_returns" : portfolio_returns,
            "performance_stats" : performance_stats}

