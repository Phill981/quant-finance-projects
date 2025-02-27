import requests
import time
from datetime import datetime

# URL for the live price data
URL = ("https://www.ls-tc.de/_rpc/json/instrument/chart/dataForInstrument"
       "?container=chart3&instrumentId=70595&marketId=1&quotetype=mid&series=intraday&type=mini&localeId=2")


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

    print("Instrument Info:")
    print("  ISIN           :", info.get("isin", "N/A"))
    print("  Chart Type     :", info.get("chartType", "N/A"))
    print("  Text Max Value :", info.get("textMaxValue", "N/A"))
    print("  Text Min Value :", info.get("textMinValue", "N/A"))
    print("\nPrice Data (timestamp : price):")
    for point in data_points:
        if len(point) >= 2:
            timestamp, price = point[0], point[1]
            # Convert timestamp (ms) to a human-readable datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            print(f"  {dt} : {price}")
    print("-" * 60)


def main():
    while True:
        data = fetch_price_data()
        if data:
            print_price_data(data)
        else:
            print("Failed to retrieve data.")
        time.sleep(1)  # update every 1 second


if __name__ == "__main__":
    main()
