# Build a web application that scrapes data related to Mission to Mars and displays the information in a single HTML page.

from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set executable path to Chrome driver and initialize browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # #### NASA Mars News

    # Visit the NASA Mars News Site and scrape the titles and paragraphs text

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_news_title = soup.find('div', class_='content_title').text
    mars_news_p = soup.find('div', class_='article_teaser_body').text
  
    # JPL Mars Space Images-Featured Image
    # Visit the JPL Mars Space Images url and scrape featured image
    url = "https://spaceimages-mars.com/" 
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_featured_image = soup.find('img', class_='headerimage fade-in')['src']
    
    mars_featured_image_url = f'https://spaceimages-mars.com/{mars_featured_image}'
    


    # Mars Facts
    # Use pandas to scrape the table containing facts about the planet including diameter, mass, etc.
    mars_facts_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    mars_facts_df.columns = ['Description', 'Mars', 'Earth']
    mars_facts_df.set_index('Description', inplace=True)
   
    # convert the dataframe to html
    mars_html = mars_facts_df.to_html()
   
    # Visit the Astrogeology site and scrape the Mars hemisphere images
    astro_site_url = 'https://marshemispheres.com/'
    browser.visit(astro_site_url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # create list of all hemispheres
    list = browser.find_by_css('a.product-item img')

    # loop through the list of hemispheres
    for i in range(len(list)):
        hemisphere_dict = {}
        
    
        browser.find_by_css('a.product-item img')[i].click()
        
        # find the url of the image
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere_dict['img_url'] = sample_elem['href']
        
        # find the title of the image
        hemisphere_dict['title'] = browser.find_by_css('h2.title').text
        
        # append the dictionary to the list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # goback to the previous page
        browser.back()
  
    # Save all the above data in the empty dict
    mars_data = {'news_title': mars_news_title ,
    'news_paragraph': mars_news_p,
    'featured_image': mars_featured_image_url,
    'facts': mars_html,
    'hemispheres': hemisphere_image_urls
    }

    # Quit the browser
    browser.quit()
    return mars_data
