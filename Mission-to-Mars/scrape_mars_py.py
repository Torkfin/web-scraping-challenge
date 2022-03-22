

# Module used to connect Python with MongoDb
import pymongo

# Web Scraping Modules
import pandas as pd
import pprint
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser

import re
from webdriver_manager.chrome import ChromeDriverManager

# NASA Mars News - Red Planet Scrape

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # URL to be scraped
    url = "https://redplanetscience.com/"
    browser.visit(url)


    # HTML object
    html = browser.html

    # Find the first title using Beautiful Soup
    soup = bs(html, "html.parser")
    latest_news = soup.find_all("div", class_="content_title")[0]

    #  Assign and print the latest title
    latest_news_title = latest_news.text

    #  Find the teaser
    paragraph = soup.find_all("div", class_="article_teaser_body")[0]

    latest_news_paragraph = paragraph.text

     # JPL Mars Images

    # URL to be scraped
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # HTML object
    html = browser.html
    soup = bs(html, "html.parser")

    # Loop through images using Beautiful Soup
    img = [img.get("src") for img in soup.find_all("img", class_="headerimage fade-in")]

    featured_image_url = url + img[0]


    # Mars Facts Scrape
    # URL to be scraped
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)

    # HTML object
    html = browser.html
    soup = bs(html, "html.parser")

    # Create the Beautiful Soup object and find all table info
    table = soup.find_all("table", class_="table table-striped")[0]

    category_header = [i.text for i in table("th")]

    measures_column = [i.text for i in table("td")]

    table_df = {"Data-Category": category_header, "Measures": measures_column}


    update_df = pd.DataFrame(table_df)
    update_df.set_index("Data-Category", inplace=True)
    update_df["Measures"] = update_df["Measures"].str.replace("\t", "")
 
    mars_table = update_df.to_html(classes="table table-striped")
    
    
        
     # Mars Hemispheres

    # URL to be scraped
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    hemisphere_image_urls = []

    for i in range(4):
        html = browser.html
        soup = bs(html, "html.parser")
    
        title = soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()
    
        html = browser.html
        soup = bs(html, "html.parser")
    
        img_url = soup.find("img", class_="wide-image")["src"]
    
        hemisphere_image_urls.append({
            "title": title,
            "img_url": hemi_url + img_url
        })
        browser.back()
        
    title1 = hemisphere_image_urls[0]["title"]
    image1 = hemisphere_image_urls[0]["img_url"]
    
    title2 = hemisphere_image_urls[1]["title"]
    image2 = hemisphere_image_urls[1]["img_url"]

    title3 = hemisphere_image_urls[2]["title"]
    image3 = hemisphere_image_urls[2]["img_url"]

    title4 = hemisphere_image_urls[3]["title"]
    image4 = hemisphere_image_urls[3]["img_url"]
    
    browser.quit()

    mars_data = {
    "latest_title": latest_news_title,
    "latest_paragraph" : latest_news_paragraph,
    "featured_image": featured_image_url,
    "html_table": mars_table,
    "hemisphere_scrape": hemisphere_image_urls,
    "title1": title1,
    "title2": title2,
    "title3": title3,
    "title4": title4,
    "image1": image1,
    "image2": image2,
    "image3": image3,
    "image4": image4,
    }

    return mars_data