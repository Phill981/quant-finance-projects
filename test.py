import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -------------------
# Configuration
# -------------------
# Set the URL of the page you want to scrape.
# Replace with the actual URL
URL = "https://www.ls-tc.de/de/aktie/tesla-motors-aktie"

# Insert the XPath for the element whose live value you want to track.
# e.g., "//div[@id='live-value']"
XPATH = '//*[@id="page_content"]/div/div[1]/div/div[2]/div[2]'

# Update interval in milliseconds (e.g., 1000ms = 1 second)
UPDATE_INTERVAL = 1000

# -------------------
# Set up Selenium WebDriver (Chrome)
# -------------------
options = webdriver.ChromeOptions()
# Uncomment the next line to run Chrome in headless mode (without opening a visible browser window)
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get(URL)

# -------------------
# Set up Tkinter GUI
# -------------------
root = tk.Tk()
root.title("Live Data Scraper")
root.geometry("400x200")
label = tk.Label(root, text="Loading...", font=("Helvetica", 24))
label.pack(expand=True, padx=20, pady=20)


def update_value():
    try:
        # Locate the element using the provided XPath and extract its text.
        element = driver.find_element(By.XPATH, XPATH)
        # Change to .get_attribute("value") if needed.
        live_value = element.text
    except Exception as e:
        live_value = f"Error: {e}"
    # Update the label in the GUI
    label.config(text=live_value)
    # Schedule the next update after UPDATE_INTERVAL milliseconds.
    root.after(UPDATE_INTERVAL, update_value)


# Start the periodic update
update_value()

# Run the Tkinter event loop
try:
    root.mainloop()
finally:
    # When the GUI is closed, quit the driver.
    driver.quit()
