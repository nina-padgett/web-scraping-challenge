# Automates browser actions
from splinter import Browser
import time
# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo
    mars = {}

    # The url we want to scrape
    url = "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Build our dictionary for the headline, price, and neighborhood from our scraped data
    mars["headline"] = soup.find("a", class_="title").get_text()
    mars["price"] = soup.find("h4", class_="price").get_text()
    mars["reviews"] = soup.find("p", class_="pull-right").get_text()

    # Quit the browser
    browser.quit()

    # Return our dictionary
    return mars