import requests
import time
from datetime import datetime
import pandas as pd

# URL for the live price data
URL = "https://www.ls-tc.de/_rpc/json/instrument/chart/dataForInstrument?container=chart3&instrumentId=70595&marketId=1&quotetype=mid&series=intraday&type=mini&localeId=2"

def fetch_price_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching data:", e)
        return None

def print_price_data(data):
    # Extract info and intraday series from the JSON
    info = data.get("info", {})
    series = data.get("series", {})
    intraday = series.get("intraday", {})
    data_points = intraday.get("data", [])

    # Create a list to store the data points
    data_list = []

    for point in data_points:
        if len(point) >= 2:
            timestamp, price = point[0], point[1]
            # Convert timestamp (ms) to a human-readable datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            data_list.append({"datetime": dt, "price": price})

    # Create a DataFrame from the list
    df = pd.DataFrame(data_list)
    return df

def mean_reversion_strategy(df, window=20, threshold=2):
    df['mean'] = df['price'].rolling(window=window).mean()
    df['std'] = df['price'].rolling(window=window).std()
    df['z_score'] = (df['price'] - df['mean']) / df['std']

    latest_z_score = df['z_score'].iloc[-1]

    if latest_z_score > threshold:
        return "Sell"
    elif latest_z_score < -threshold:
        return "Buy"
    else:
        return "Hold"

def backtest_strategy(df, window=20, threshold=2):
    df['mean'] = df['price'].rolling(window=window).mean()
    df['std'] = df['price'].rolling(window=window).std()
    df['z_score'] = (df['price'] - df['mean']) / df['std']

    df['signal'] = df['z_score'].apply(lambda x: "Sell" if x > threshold else ("Buy" if x < -threshold else "Hold"))
    df['position'] = df['signal'].shift()
    df['position'] = df['position'].fillna('Hold')

    df['returns'] = df['price'].pct_change()
    df['strategy_returns'] = df['returns'] * df['position'].apply(lambda x: 1 if x == 'Buy' else (-1 if x == 'Sell' else 0))

    cumulative_returns = (df['strategy_returns'] + 1).cumprod() - 1
    return cumulative_returns.iloc[-1]
    
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

def main():
    while True:
        data = fetch_price_data()
        timestamp = timestamp_to_datetime(data["series"]["intraday"]["data"][-1][0])
        if data:
            df = print_price_data(data)
            if not df.empty:
                signal = mean_reversion_strategy(df)
                print(f"{timestamp} Signal: {signal}")
                backtest_result = backtest_strategy(df)
                print(f"Backtest Cumulative Return: {backtest_result:.2%}")
        time.sleep(1)

if __name__ == "__main__":
    main()
