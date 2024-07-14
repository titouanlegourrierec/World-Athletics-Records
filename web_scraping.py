"""
Web Scraping Utility for Athletic Records

This script contains functions for scraping athletic records from World Athletics web pages and saving the data to CSV files.
It uses BeautifulSoup for parsing HTML content and Selenium for web page interaction.

Author: LE GOURRIEREC Titouan
"""

############################################################################################################

from datetime import datetime
import logging
import time

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

############################################################################################################
##############################           Web scraping functions           ##################################
############################################################################################################

def create_csv(content : str, csv_name : str) -> None:
    """
    Extracts athletic records from HTML and saves to a CSV.

    Parameters:
        - content (str): HTML content.
        - csv_name (str): Output CSV file name.
    """

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    # Find the table containing the records
    table_body = soup.find(attrs={'class':'Table_table__2zsdR RecordsTable_table__3X8lL'}).find('tbody')
    # Find all table rows
    rows = table_body.find_all('tr')

    data = {
        'DISCIPLINE': [],
        'PERF': [],
        'COMPETITOR': [],
        'DOB': [],
        'COUNTRY': [],
        'VENUE': [],
        'DATE': []
    }

    for row in rows:
        cells = row.find_all('td')
        data['DISCIPLINE'].append(cells[0].text.strip())
        
        perf = cells[2].text.strip()
        for r in ["*", "Mx", "Wo", "h"]:
            perf = perf.replace(r, "")
        data['PERF'].append(perf.strip())

        data['COMPETITOR'].append(cells[4].text.strip())
        data['DOB'].append(cells[5].text.strip())
        data['COUNTRY'].append(cells[6].text.strip())
        data['VENUE'].append(cells[7].text.strip().replace("(i)", ""))
        data['DATE'].append(cells[8].text.strip())

    records = pd.DataFrame(data)
    records.to_csv(csv_name, index=False)


def click_button(driver: webdriver.Chrome, xpath: str) -> None:
    """
    Clicks a button identified by an XPath on a webpage using Selenium WebDriver.

    Parameters:
        - driver: The Selenium WebDriver instance used to interact with the webpage.
        - xpath (str): The XPath string used to locate the button on the webpage.

    Exceptions:
        - Exception: Catches and prints any exception that occurs during the button click attempt, then quits the driver
        and asserts False to indicate failure.
    """
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
    except Exception as e:
        print(f"Error during the click button: {e}")
        driver.quit()
        assert False


def get_content_and_create_csv(driver: webdriver.Chrome, url: str, button_selector: str, csv_name: str) -> None:
    """
    Navigates to a URL, optionally clicks a button, and creates a CSV from the page content.

    Parameters:
        - driver: Selenium WebDriver used for web page navigation and interaction.
        - url (str): The URL of the web page to navigate to.
        - button_selector (str): XPath selector for a button to click after loading the page. If None, no button is clicked.
        - csv_name (str): Name of the CSV file to be created with the content from the web page.
    """
    driver.get(url)
    if button_selector:
        click_button(driver, button_selector)
    content = driver.page_source
    create_csv(content, csv_name)


############################################################################################################
#############################             Web scraping script             ##################################
############################################################################################################

def main():

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    categories = [
        ("world-records", "world_records"),
        ("olympic-games-records", "olympic_games_records"),
        ("african-records", "african_records"),
        ("asian-records", "asian_records"),
        ("european-records", "european_records"),
        ("nacac-records", "nacac_records"),
        ("oceanian-records", "oceanian_records"),
        ("south-american-records", "south_american_records")
    ]

    men_button = '//*[@id="__next"]/div[3]/div/div/div[2]/ul/li[2]/button'

    with webdriver.Chrome(options=chrome_options) as driver:
        for category, file_name in categories:
            base_url = "https://worldathletics.org/records/by-category/"
            logging.info(f"Processing category: {category}")
            get_content_and_create_csv(driver, f"{base_url}{category}", None, f"data/data_after/women_{file_name}.csv")
            get_content_and_create_csv(driver, f"{base_url}{category}", men_button, f"data/data_after/men_{file_name}.csv")

            logging.info(f"Files data/data_after/women_{file_name}.csv and data/data_after/men_{file_name}.csv have been created successfully.")

if __name__ == "__main__":
    main()