#!/usr/bin/env python3


"""
backtest_portfolio_prompts.py:
"""

from typing import List
from resources.data_resources import available_tickers
from server import mcp


@mcp.prompt("backtest_portfolio")
def backtest_portfolio(tickers: str, weights: str) -> str:
    """
        Backtest a portfolio given a list of tickers and their weights.
    Args:
        tickers (str): Comma-separated string of ticker symbols.
        weights (str): Comma-separated string of weights corresponding to the tickers.
    Returns:
    """
    tickers_univ = available_tickers()
    input_tickers = tickers.split(",")
    input_weights = weights.split(",")
    if len(input_tickers) != len(input_weights):
        raise ValueError("Number of tickers must match number of weights.")

    tickers_to_use = []
    ticker_weights = []
    unavailable_tickers = []
    for i,ticker in enumerate(input_tickers):
        ticker = ticker.upper().strip()
        if ticker not in tickers_univ:
            unavailable_tickers.append(ticker)
        else:
            tickers_to_use.append(ticker)
            ticker_weights.append(float(input_weights[i].replace("%", "")))
    if len(tickers_to_use) == 0:
        raise ValueError(f"None of the requested tickers {input_tickers} are available in the data.")
    ticker_weights = [w * 100/ sum(ticker_weights) for w in ticker_weights]  # Normalize weights
    #portfolio = dict(zip(tickers_to_use, ticker_weights))
    portfolio_str = ", ".join([f"{weight:.2f}% to {ticker}" for ticker, weight in zip(tickers_to_use, ticker_weights)])
    return f"""
        Please use the tools you have and run a backtest for a portfolio that allocates 
            {portfolio_str}
        and then display some useful charts and tables from the result.
    """
