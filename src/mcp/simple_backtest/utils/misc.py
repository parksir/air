#!/usr/bin/env python3
"""
Portfolio Backtesting Utils

This script provides three main tools:
1. get_price_data: Retrieves price data from CSV for given tickers
2. backtest_portfolio: Runs portfolio backtest and returns time series
3. calculate_performance_stats: Computes performance metrics from returns
"""

import logging
from typing import Any, Dict, List, Optional, Sequence
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio-mcp-server")


def load_price_data(csv_file_path: str) -> pd.DataFrame:
    """Load price data from CSV file."""
    try:
        df = pd.read_csv(csv_file_path)
        
        # Ensure we have a Date column and set it as index
        if 'Date' not in df.columns:
            raise ValueError("CSV file must contain a 'Date' column")
        
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        logger.info(f"Loaded price data with shape: {df.shape}")
        logger.info(f"Available columns: {df.columns.tolist()}")
        
        return df
    except Exception as e:
        logger.error(f"Error loading price data: {str(e)}")
        raise

def get_ticker_data(df: pd.DataFrame, tickers: List[str]) -> pd.DataFrame:
    """Extract data for specific tickers from the dataframe."""
    available_tickers = [col for col in tickers if col in df.columns]
    missing_tickers = [col for col in tickers if col not in df.columns]
    
    if missing_tickers:
        logger.warning(f"Missing tickers: {missing_tickers}")
    
    if not available_tickers:
        raise ValueError(f"None of the requested tickers {tickers} are available in the data")
    
    return df[available_tickers].copy()

def calculate_portfolio_returns(price_data: pd.DataFrame, weights: Dict[str, float]) -> pd.Series:
    """Calculate portfolio returns given price data and weights."""
    # Calculate daily returns
    returns = price_data.pct_change().dropna()
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    normalized_weights = {ticker: weight/total_weight for ticker, weight in weights.items()}
    
    # Calculate weighted portfolio returns
    portfolio_returns = pd.Series(0.0, index=returns.index)
    
    for ticker, weight in normalized_weights.items():
        if ticker in returns.columns:
            portfolio_returns += returns[ticker] * weight
    
    return portfolio_returns

def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
    """Calculate cumulative returns from raw returns."""
    return (1 + returns).cumprod() - 1

def calculate_performance_metrics(returns: pd.Series) -> Dict[str, float]:
    """Calculate comprehensive performance statistics for a return series."""
    if len(returns) == 0:
        return {}
    
    # Basic statistics
    total_return = (1 + returns).prod() - 1
    
    # Annualized metrics (assuming monthly data)
    trading_days = 12 # 252
    periods_per_year = trading_days
    
    # Handle the case where we have less than a year of data
    years = len(returns) / periods_per_year
    
    if years > 0:
        annualized_return = (1 + total_return) ** (1/years) - 1
    else:
        annualized_return = 0.0
    
    annualized_volatility = returns.std() * np.sqrt(periods_per_year)
    
    # Sharpe ratio (assuming risk-free rate of 0)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0.0
    
    # Maximum drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Downside deviation and Sortino ratio
    negative_returns = returns[returns < 0]
    downside_deviation = negative_returns.std() * np.sqrt(periods_per_year)
    sortino_ratio = annualized_return / downside_deviation if downside_deviation != 0 else 0.0
    
    # Win rate
    win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0.0
    
    # Calmar ratio
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0.0
    
    # VaR and CVaR (5% level)
    var_5 = returns.quantile(0.05)
    cvar_5 = returns[returns <= var_5].mean()
    
    return {
        "total_return": float(total_return),
        "annualized_return": float(annualized_return),
        "annualized_volatility": float(annualized_volatility),
        "sharpe_ratio": float(sharpe_ratio),
        "sortino_ratio": float(sortino_ratio),
        "max_drawdown": float(max_drawdown),
        "calmar_ratio": float(calmar_ratio),
        "win_rate": float(win_rate),
        "var_5_percent": float(var_5),
        "cvar_5_percent": float(cvar_5),
        "skewness": float(returns.skew()),
        "kurtosis": float(returns.kurtosis()),
        "num_periods": len(returns),
        "years_of_data": float(years)
    }
 

#if __name__ == "__main__":
def test():
    portfolio = {
        'AGG': 0.3,
        'EFA': 0.15, 
        'EEM': 0.05, 
        'SPY': 0.5,
    }
    # Load price data
    df = load_price_data('/tmp/test_price_data.csv')
    # Get tickers from portfolio
    tickers = list(portfolio.keys())
    
    # Get price data for portfolio tickers
    price_data = get_ticker_data(df, tickers)
    
    # Calculate portfolio returns
    portfolio_returns = calculate_portfolio_returns(price_data, portfolio)
    
    # Calculate performance metrics
    stats = calculate_performance_metrics(portfolio_returns)
    print(stats)