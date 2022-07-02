from flask import Flask, render_template, redirect
from splinter import Browser
import os
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time
import datetime as dt


def scrape_all():
    
# Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    latest_news_title, latest_news_paragraph = latest_news_title_and_paragraph_function(browser)

    all_scraped_elements_dict = {"latest_news_title": latest_news_title, 
                                "latest_news_paragraph": latest_news_paragraph, 
                                "featured_image_url": mars_featured_img_function(browser), 
                                "facts_html": mars_facts_function(),
                                "hemispheres": hemispheres(browser),
                                "last_modify": dt.datetime.now()}
    browser.quit
    return all_scraped_elements_dict
   
# Create a function to extract the latest news title
def latest_news_title_and_paragraph_function(browser):
    # Use browser to visit the URL
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Wait 1 seconds
    time.sleep(1)

    # Retrieve page
    html = browser.html

    # Create Beautiful Soup Object
    news_soup = bs(html, 'html.parser')
    type(news_soup)

    latest_news_title = news_soup.find('div', class_='content_title').get_text()

    # Extract paragraph text of the latest news story
    latest_news_paragraph = news_soup.find('div', class_='article_teaser_body').get_text()
    return latest_news_title, latest_news_paragraph


# Create a function to extract the Mars Space Featured Image
def mars_featured_img_function(browser):
    # Use browser to visit the URL
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    full_img = browser.find_by_tag("button")[1]
    full_img.click()

    # Retrieve page
    html = browser.html

    # Create Beautiful Soup Object
    image_soup = bs(html, 'html.parser')
   
    # error handling
    try:
        featured_image_url = image_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    image_url=f'https://spaceimages-mars.com/{featured_image_url}'
    return image_url


# Create a function to extract Mars Facts
def mars_facts_function():
    try: 
        facts_url = 'https://galaxyfacts-mars.com/'
        df = pd.read_html(facts_url)[0]
    except BaseException:
        return None

    # Wait 1 second
    time.sleep(1)

    # Read html table
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Clean table by removing unwanted newlines 
    facts_html = df.to_html(classes='table table-striped')
    return facts_html
    facts_soup = bs(html, '')


# Create a function to extract Mars Hemisphere Images
def hemispheres(browser):
    all_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(all_hemispheres_url + 'index.html')
    stored_img_urls = []
    
    for i in range(4):

        browser.find_by_css('a.product-item img')[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data["img_url"] = all_hemispheres_url + hemi_data["img_url"]
        stored_img_urls.append(hemi_data)
        browser.back()
    return stored_img_urls

def scrape_hemisphere(html_text):
    hemi_soup = bs(html_text, "html.parser")
    try:
        title_elements = hemi_soup.find("h2", class_="title").get_text()
        sample_elements = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_elements = None
        sample_elements = None
    
    hemispheres = {"title":title_elements, "img_url":sample_elements}
    return hemispheres

#scrape_all()
if __name__ == "__main__":
    print(scrape_all())