import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ANSI color codes for terminal output
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

# -------------------
# Configuration
# -------------------
stocks = {
    "Tesla": "https://www.ls-tc.de/de/aktie/tesla-motors-aktie",
    "Apple": "https://www.ls-tc.de/de/aktie/apple-aktie",
    "NVIDIA": "https://www.ls-tc.de/de/aktie/nvidia-dl-01-aktie"
}

# XPaths for bid (Geld) values (assumed same structure on each page)
bid_value_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[2]/div/span'
bid_amount_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[2]/span/span'
bid_currency_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[2]/div/text()'

# XPaths for ask (Brief) values
ask_value_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[3]/div/span'
ask_amount_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[3]/div/span'
ask_currency_xpath = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[3]/div/text()'

UPDATE_INTERVAL = 1  # seconds

# -------------------
# Set up Selenium WebDriver (Chrome) for each stock
# -------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")

drivers = {}
for stock_name, url in stocks.items():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(url)
    drivers[stock_name] = driver


def get_text_via_xpath(driver, xpath):
    """Retrieve a text value using JavaScript evaluation for XPath expressions ending in /text()."""
    return driver.execute_script(
        "return document.evaluate(arguments[0], document, null, XPathResult.STRING_TYPE, null).stringValue;",
        xpath
    )


# Dictionary to store last prices for comparison (per stock)
last_prices = {stock: {"bid": None, "ask": None} for stock in stocks}

try:
    while True:
        output_lines = []
        for stock_name, driver in drivers.items():
            # Since the page updates automatically, we simply query the current values
            # Get bid (Geld) data
            try:
                bid_text = driver.find_element(By.XPATH, bid_value_xpath).text
                bid_amount = driver.find_element(
                    By.XPATH, bid_amount_xpath).text
                bid_currency = get_text_via_xpath(driver, bid_currency_xpath)
                new_bid = float(bid_text.replace(",", ".").strip())
            except Exception as e:
                bid_text = bid_amount = bid_currency = f"Error: {e}"
                new_bid = None

            # Get ask (Brief) data
            try:
                ask_text = driver.find_element(By.XPATH, ask_value_xpath).text
                ask_amount = driver.find_element(
                    By.XPATH, ask_amount_xpath).text
                ask_currency = get_text_via_xpath(driver, ask_currency_xpath)
                new_ask = float(ask_text.replace(",", ".").strip())
            except Exception as e:
                ask_text = ask_amount = ask_currency = f"Error: {e}"
                new_ask = None

            # Determine color for bid based on previous value
            last_bid = last_prices[stock_name]["bid"]
            if new_bid is not None and last_bid is not None:
                if new_bid > last_bid:
                    bid_color = COLOR_GREEN
                elif new_bid < last_bid:
                    bid_color = COLOR_RED
                else:
                    bid_color = COLOR_YELLOW
            else:
                bid_color = COLOR_RESET

            # Determine color for ask based on previous value
            last_ask = last_prices[stock_name]["ask"]
            if new_ask is not None and last_ask is not None:
                if new_ask > last_ask:
                    ask_color = COLOR_GREEN
                elif new_ask < last_ask:
                    ask_color = COLOR_RED
                else:
                    ask_color = COLOR_YELLOW
            else:
                ask_color = COLOR_RESET

            # Save new prices for next comparison
            if new_bid is not None:
                last_prices[stock_name]["bid"] = new_bid
            if new_ask is not None:
                last_prices[stock_name]["ask"] = new_ask

            stock_output = (
                f"Stock: {stock_name}\n"
                f"  Bid: {bid_color}{bid_text}{COLOR_RESET} | Amount: {bid_amount} | Currency: {bid_currency}\n"
                f"  Ask: {ask_color}{ask_text}{COLOR_RESET} | Amount: {ask_amount} | Currency: {ask_currency}\n"
                + "-" * 60
            )
            output_lines.append(stock_output)

        # Clear the console and print updated values
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\n".join(output_lines))
        time.sleep(UPDATE_INTERVAL)
finally:
    for driver in drivers.values():
        driver.quit()
