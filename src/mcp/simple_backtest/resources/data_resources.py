#!/usr/bin/env python3


"""
data_resources.py:
    1. load_price_data: Load price data from CSV file
    2. get_ticker_data: Extract data for specific tickers from the dataframe
    3. calculate_portfolio_returns: Calculate portfolio returns given price data and weights
"""

from typing import List
from utils.misc import (
    load_price_data
)
from server import mcp
from tools.data_tools import DEFAULT_CSV_PATH


@mcp.resource("data://tickers")
def available_tickers() -> List[str]:
    """
    Retrieve available tickers from the price data CSV file.
    
    Args:
        None
    
    Returns:
        list of str: List of available ticker symbols.
    """
    df = load_price_data(DEFAULT_CSV_PATH)
    return df.columns.tolist()
