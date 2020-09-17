import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict = {}

    # News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('li', class_='slide').find('div', class_='content_title').text
    paragraph = soup.find('li', class_='slide').find('div', class_='article_teaser_body').text
    mars_dict['news_title'] = title
    mars_dict['news_paragraph'] = paragraph

    # -------------------------------------------------------

    # Featured Image
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.find_by_id('full_image').first.click()
    browser.links.find_by_text("more info     ").first.click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.select_one('figure.lede a img').get("src")
    featured_img_url = 'https://www.jpl.nasa.gov/' + image_url
    mars_dict["featured_image"] = featured_img_url

    # -------------------------------------------------------

    # Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'html.parser').find_all(
        'a', class_='itemLink')
    hemi_titles = []
    for x in soup:
        title = x.find('h3').text
        hemi_titles.append(title)
    hemi_titles
    browser.visit(url)
    hemi_imglist = []
    for x in range(len(hemi_titles)):
        browser.visit(url)
        try:
            browser.click_link_by_partial_text(hemi_titles[x])
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_text(hemi_titles[x])
        html = browser.html
        soup2 = BeautifulSoup(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']
        # urls.append(hemi_url)
        hemi_dict = {"title": hemi_titles[x], 'img_url': hemi_url}
        hemi_imglist.append(hemi_dict)
        mars_dict['hemi_imgs'] = hemi_imglist
        
    #Space Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    

    df = tables[1]
    df

    html_table = df.to_html()
    mars_dict['tables'] = html_table

    return mars_dict
