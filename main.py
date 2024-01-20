from functions import *

if __name__ == "__main__":
    client = api.Binance_API(api_key=binance_api_key, secret_key=binance_secret_key)

    start_date = "2023-01-01"
    end_date = "2025-12-31"

    timeframe = "4h"
    pair1 = "TRXUSDT"
    pair2 = "BANDUSDT"


    # Download single asset data
    candles = get_candles_batched(client, symbol=pair1, interval=timeframe, start_date=start_date, end_date=end_date, delay=0.4)
    df = create_df(candles)

    print(df)
    plot_chart(df)
    df.to_csv(f"df_{timeframe}_{pair1}.csv", index=False)


    # # Download spread data
    # candles1 = get_candles_batched(client, symbol=pair1, interval=timeframe, start_date=start_date, end_date=end_date, delay=0.4)
    # candles2 = get_candles_batched(client, symbol=pair2, interval=timeframe, start_date=start_date, end_date=end_date, delay=0.4)

    # df_spread = create_spread_df(candles1, candles2)
    # print(df_spread)
    # plot_chart(df_spread)
    # df_spread.to_csv(f"df_spread_{timeframe}_{pair1}_{pair2}.csv", index=False)
