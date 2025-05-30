# main.py

from server import mcp

import tools.data_tools
import tools.backtest_tools

import prompts.backtest_portfolio_prompts

import resources.data_resources


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
