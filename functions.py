import time
import numpy as np
import datetime
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import api
from keys import *

def to_timestamp(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    timestamp = datetime.timestamp(date_object)
    timestamp_ms = int(timestamp * 1000)
    return timestamp_ms

def get_candles_batched(client, symbol, interval, start_date, end_date, delay=0.4):
    start_timestamp = to_timestamp(start_date)
    end_timestamp = to_timestamp(end_date)
    limit = 1500  # Maximum candle limit for one request

    interval_ms = {
        "1m": 60000,  # 1 min
        "5m": 300000,  # 5 min
        "15m": 900000,  # 15 min
        "30m": 1800000,  # 30 min
        "1h": 3600000,  # 1 hour
        "4h": 14400000,  # 4 hours
        "1d": 86400000  # 1 day
    }[interval]


    candles = []
    current_timestamp = start_timestamp

    # Calculate the total number of batches
    total_batches = (end_timestamp - start_timestamp) // (limit * interval_ms)

    # Create a tqdm progress bar
    with tqdm(total=total_batches) as pbar:
        while current_timestamp < end_timestamp:

            end_of_batch = current_timestamp + limit * interval_ms
            if end_of_batch > end_timestamp:
                end_of_batch = end_timestamp

            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit,
                "startTime": current_timestamp,
                "endTime": end_of_batch
            }

            batch_candles = client.get_candles_with_data(symbol=symbol, interval=interval, startTime=current_timestamp, endTime=end_of_batch, limit=limit)
            candles.extend(batch_candles)

            current_timestamp = end_of_batch
            time.sleep(delay)

            # Update the progress bar
            pbar.update(1)

    return candles

def create_spread_df(candles1, candles2):

    df1 = pd.DataFrame(data=candles1,
                       columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                'taker_buy_quote_asset_volume', 'ignore'])
    df1 = df1.loc[:, ['timestamp', 'open', 'high', 'low', 'close']]

    df2 = pd.DataFrame(data=candles2,
                       columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                'taker_buy_quote_asset_volume', 'ignore'])
    df2 = df2.loc[:, ['timestamp', 'open', 'high', 'low', 'close']]

    df1['open'] = pd.to_numeric(df1['open'], errors='coerce')
    df1['low'] = pd.to_numeric(df1['low'], errors='coerce')
    df1['high'] = pd.to_numeric(df1['high'], errors='coerce')
    df1['close'] = pd.to_numeric(df1['close'], errors='coerce')

    df2['open'] = pd.to_numeric(df2['open'], errors='coerce')
    df2['low'] = pd.to_numeric(df2['low'], errors='coerce')
    df2['high'] = pd.to_numeric(df2['high'], errors='coerce')
    df2['close'] = pd.to_numeric(df2['close'], errors='coerce')

    df1 = df1.dropna()
    df2 = df2.dropna()

    spread_c = df1['close'] / df2['close']
    spread_h = df1['high'] / df2['high']
    spread_l = df1['low'] / df2['low']
    spread_o = df1['open'] / df2['open']

    spread_data = {'timestamp': df1['timestamp'],  'open': spread_o, 'high': spread_h, 'low': spread_l, 'close': spread_c}
    df_spread = pd.DataFrame(data=spread_data)

    return df_spread

def create_df(candles):

    df = pd.DataFrame(data=candles,
                       columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                'taker_buy_quote_asset_volume', 'ignore'])
    df = df.loc[:, ['timestamp', 'open', 'high', 'low', 'close']]

    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    df = df.dropna()
    df = pd.DataFrame(data=df)

    return df

def plot_chart(df):

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.5])

    # Plot candlesticks on the first row
    fig.add_trace(go.Candlestick(x=df['timestamp'], open=df['open'], high=df['high'], low=df['low'], close=df['close'], name='Candlesticks'), row=1, col=1)

    fig.update_layout(title='Chart ', xaxis_title='Timestamp', xaxis_rangeslider_visible=False)
    fig.show()




