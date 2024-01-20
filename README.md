## Binance Data Downloader

This code is a tool for downloading and visualizing historical data of cryptocurrency pairs from the Binance exchange. The code allows the user to get candlestick data on selected trading pairs for an unlimited or specified period of time to build candlestick charts.

A problem when downloading data from the Binance exchange is the limit of 1500 bars for a single request. This tool effectively overcomes this limitation by allowing the user to select the desired timeframe and download data for, for example, 1, 2 or 3 years much more efficiently and quickly. The result is a ready-made dataframe with complete data obtained from the exchange.

### Features

- Obtain candlestick data for the selected cryptocurrency pair and time frame using Binance API.
- Creating a spread dataframe from two assets
- Building a candlestick chart for visual analysis of previously obtained data
- Ability to save the obtained data in CSV format for further use or analysis.

### How to run
1. Specify your API and secret key in the keys.py file
2. Run the main.py script to load the data and plot the graphs.
3. Save the obtained data to CSV files for further analysis or use using the appropriate function

## Images

Example of TRXUSDT asset data download and chart output from 2020 on 1h timeframe

![newplot (6)](https://github.com/nonisich/Binance-Data-Downloader/assets/109261916/2a2b28d6-6a04-4f55-8593-80ead9ff6195)
