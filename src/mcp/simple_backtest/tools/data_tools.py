#!/usr/bin/env python3

"""
tools/data_tools.py:
    1. get_price_data: Retrieves price data from CSV for given tickers
"""

import pandas as pd
from server import mcp
from utils.misc import (
    load_price_data,
    get_ticker_data
)

# Global variable to store the default CSV file path
DEFAULT_CSV_PATH = "/tmp/test_price_data.csv"

@mcp.tool()
def get_price_data(tickers, price_data_path=DEFAULT_CSV_PATH) -> pd.DataFrame:
    """ 
        Retrieve price data for specified tickers from a CSV file.

    Args:
        tickers (list): List of ticker symbols to retrieve data for.
        price_data_path (str): Path to the CSV file containing price data.

    Returns:
        pd.DataFrame: DataFrame containing price data for the specified tickers.
    """
    # Load price data
    df = load_price_data(price_data_path)
    # Get data for specified tickers
    return get_ticker_data(df, tickers)
