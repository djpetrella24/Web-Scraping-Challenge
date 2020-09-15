
def scrape(): 
    import pandas as pd
    import pymongo
    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict = {}


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    step_one = soup.select_one('ul.item_list li.slide')
    title = step_one.find('div', class_='content_title').text
    paragraph = step_one.find('div', class_='article_teaser_body').text

    mars_dict['title'] = title
    mars_dict['paragraph'] = paragraph

    return mars_dict