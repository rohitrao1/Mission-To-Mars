
# Dependencies
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs 
import requests
#import pymongo
from splinter import Browser

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_ = 'content_title').text
    news_p = soup.find('div', class_ = 'article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = soup.find("a", class_ = "button fancybox")["data-fancybox-href"]
    full_url = base_url + featured_image_url

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)
    facts_df = tables[0]
    facts_df.columns = ['Fact', 'Value']
    facts_df['Fact'] = facts_df['Fact'].str.replace(':', '')
    facts_html = facts_df.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="description")
    sites = []
    for result in results:
        link = result.find('a', class_ = "itemLink product-item")
        link_text = link['href']
        full_url = base_url + link_text
        sites.append(full_url)
    hemispheres = []
    for site in sites:
        browser.visit(site)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_ = "title").text.strip()
        url = soup.find_all('a', target = "_blank", href = True)[1]['href']
        hemispheres.append({"title": title, "img_url": url})
    
    output = {
        "news_title": news_title, 
        "news_p": news_p, 
        "featured_image_url": full_url,
        "mars_weather": mars_weather, 
        "facts_html": facts_html,
        "hemispheres": hemispheres
    }
    return output
