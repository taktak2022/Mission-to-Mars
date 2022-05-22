#!/usr/bin/env python
# coding: utf-8

# MODULE 10.3.3 Import Splinter and BeautifulSoup; IMPORT SCRAPING TOOLS
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# SET YOUR EXECUTABLE PATH; SET UP SPLINTER
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# MODULE 10.5.2 UPDATE THE CODE; INSERT CURRENT CODE INTO A FUNCTION
def mars_news(browser):

    # Visit the mars nasa news site; ASSIGN THE URL & INSTRUCT THE BROWSER TO VISIT IT
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # SET UP THE HTML PARSER
    html = browser.html
    news_soup = soup(html, 'html.parser')


    # Add try/except for error handling

    try:

        # THE SPECIFIC DATA IS IN A <div /> WITH A CLASS OF 'content_title'
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        # MODULE 10.3.3 GET THE MOST RECENT TITLE PUBLISHED ON THE WEBSITE
        # NOTE: AS WEBSITE IS UPDATED WITH NEW ARTICLES, OUTPUT WILL RETURN WITH NEWEST TITLE
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # MODULE 10.3.4 Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    # AUTOMATED BROWER WILL AUTOMATICALLY "CLICK" THE BUTTON TO CHANGE THE VIEW
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup;  NEED TO FIND THE RELATIVE IMAGE URL
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # ADD TRY/EXCEPT FOR ERROR HANDLING
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    # ADD TRY/EXCEPT FOR ERROR HANDLING
    try:
        # MODULE 10.3.5 SCRAPE DATA ABOUT MARS; 
        # WEBSCRAPING AN ENTIRE TABLE;  USE .read_html() FUNCTION
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    
    # ASSIGN COLUMNS AND SET INDEX OF DATAFRAME
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # CONVERT DATAFRAME INTO HTML FORMAT, ADD BOOTSTRAP
    return df.to_html()


# END OF MODULE 10.3.5 END THE AUTOMATED BROWSER SESSION
browser.quit()




