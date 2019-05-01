#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars
# ## Part 1: Initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

# In[68]:


# import libraries
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests




# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# get_ipython().system('which chromedriver')

def starting_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


mars_info = {}


# Nasa Mars News

def scrape():
    try:
        browser= starting_browser()

    # Nasa news URL
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    # HTML Object
    html = browser.html


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve page with the requests 
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #Dictionary
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p


    return mars_info

finally:

    browser.quit()



### JPL Mars Space Images - Featured Image
def scrape_image():

    try: 
        browser=starting_browser()

        # Use splinter to visit URL Images
        featured_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image)

        # HTML Object 
        html = browser.html

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concat web url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url
 
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    
    finally:

        browser.quit()

# ### Mars Weather

def scrape_weather():
    try:

        browser=starting_browser()

        # Mars Weather Twitter w/ splinter
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        #Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Elements that have tweets
        tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass
    
        return mars_info
    finally:
        browser.quit()


### Mars Facts
def scrape_facts():


    #Mars facts url 
    facts = 'http://space-facts.com/mars/'

    # Parse url
    mars_facts = pd.read_html(facts)



    # Mars facts DF
    mars = mars_facts[0]

    # Assign columns
    mars.columns = ['Description','Value']

    # Set the index 
    mars.set_index('Description', inplace=True)

    # Save html code
    mars.to_html()


# Display mars_df
    return mars




### Mars Hemispheres

def scrape_hems():
    try:
        browser=starting_browser()

        # Hemispheres URL
        hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres)

        # HTML Object
        html_hemispheres = browser.html

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all hemispheres info
        items = soup.find_all('div', class_='item')

        # Create hemisphere list
        hemispheres_image_urls = []

        # Store
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        # Loop through stored items
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of each hemisphere web
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemispheres_image_urls.append({"title" : title, "img_url" : img_url})
    


            mars_info['hemispheres_image_urls'] = hemispheres_image_urls

        
        # Return mars_data 
        return mars_info
    finally:

        browser.quit()




