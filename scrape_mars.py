
# coding: utf-8

# In[9]:


import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import cssutils as css


# In[10]:


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)


# In[2]:


# Article about Mars
def scrape_nasa():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    nasa = {}

    nasa["headline"] = soup.find('div', class_='content_title').text
    nasa["article"] = soup.find('div', class_='rollover_description_inner').text
     
    a_tab = soup.find('li', class_='slide').find('a')
    article_link = a_tab.get('href')
    nasa_url='https://mars.nasa.gov'
    
    nasa['article_url']=f'{nasa_url}{article_link}'
    
    return nasa


# In[3]:


# Featured Pictures of Mars
def scrape_jpl():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    div_style = soup.find('article')['style']
    style = css.parseStyle(div_style)
    pic_link = style['background-image']

    pic_link_clean = pic_link.replace('url(', '').replace(')', '')
    featured_pic_url = f'https://www.jpl.nasa.gov{pic_link_clean}'
    
    jpl={'featured_pic_url':featured_pic_url}
    
    return jpl


# In[4]:


# Mars Weather
def scrape_twitter():
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather=[]

    weather_search = soup.find_all('div', class_='js-tweet-text-container')

    for w in weather_search:
        if 'Sol' in w.text:
            weather.append(w.text)
            break    
        else:
            continue
        

    mars_weather = [w.strip() for w in weather]
    mars_weather=str(mars_weather[0])
    
    twitter={'mars_weather': mars_weather}
    
    return twitter


# In[5]:


# Facts about Mars
def scrape_facts():
    browser = init_browser()
    url = 'http://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    tables

    mars_df = tables[0]
    mars_df.columns = ['Category','Stat']
    mars_df
    
    mars_html_table = mars_df.to_html(index=False)
    mars_html_table.replace('\n', '')
    

    facts={'mars_html_table': mars_html_table}
    
    return facts


# In[15]:


# Visualizations of Mars' Hemispheres
def hemi():
    hemis={}
    Cerberus_url = 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'
    Schiaparelli_url = 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'
    Syrtis_Major_url = 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'
    Valles_Marineris_url = 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'

    Cerberus = {'title': 'Cerberus Hemisphere', 'img_url': Cerberus_url}
    Schiaparelli = {'title': 'Schiaparelli Hemisphere', 'img_url': Schiaparelli_url}
    Syrtis_Major = {'title': 'Syrtis Major Hemisphere', 'img_url': Syrtis_Major_url}
    Valles_Marineris = {'title': 'Valles Marineris Hemisphere', 'img_url': Valles_Marineris_url}
    
    hemis_list=[Cerberus, Schiaparelli, Syrtis_Major, Valles_Marineris]
    hemis={'hemi': hemis_list}
    
    return hemis