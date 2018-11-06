
# coding: utf-8

# ## Dependencies

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


from bs4 import BeautifulSoup as bs 
import requests
import pymongo


# In[3]:


from splinter import Browser


# In[4]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# ---

# ## NASA Mars News

# In[56]:


get_ipython().system('which chromedriver')


# In[57]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[59]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[67]:


html = browser.html
soup = bs(html, 'html.parser')
news_title = soup.find('div', class_ = 'content_title').text
news_p = soup.find('div', class_ = 'article_teaser_body').text
print("Title: ", news_title)
print("Description: ", news_p)


# ---

# ## JPL Mars Space Images - Featured Image

# In[5]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[90]:


url = 'https://www.jpl.nasa.gov/spaceimages/'
browser.visit(url)


# In[99]:


html = browser.html
soup = bs(html, 'html.parser')
#featured_image_url = soup.find('article')["style"]
#print(featured_image_url)
base_url = 'https://www.jpl.nasa.gov'
featured_image_url = soup.find("a", class_ = "button fancybox")["data-fancybox-href"]
full_url = base_url + featured_image_url
print(full_url)


# ---

# ## Mars Weather

# In[6]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[7]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[14]:


html = browser.html
soup = bs(html, 'html.parser')
mars_weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
print(mars_weather)


# ---

# ## Mars Facts 

# In[15]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[16]:


url = 'https://space-facts.com/mars/'
browser.visit(url)


# In[31]:


#html = browser.html
#soup = bs(html, 'html.parser')
tables = pd.read_html(url)
tables


# In[38]:


facts_df = tables[0]
facts_df.columns = ['Fact', 'Value']
facts_df['Fact'] = facts_df['Fact'].str.replace(':', '')
facts_df


# ---

# ## Mars Hemispheres

# In[5]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[69]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[88]:


html = browser.html
soup = bs(html, 'html.parser')
results = soup.find_all('div', class_="description")
sites = []
for result in results:
    link = result.find('a', class_ = "itemLink product-item")
    link_text = link['href']
    full_url = base_url + link_text
    sites.append(full_url)
sites


# In[89]:


hemispheres = []
for site in sites:
    browser.visit(site)
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find('h2', class_ = "title").text.strip()
    url = soup.find_all('a', target = "_blank", href = True)[1]['href']
    hemispheres.append({"title": title, "img_url": url})
hemispheres

