import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {'executable_path': 'C:/Windows/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
#----------NASA Mars---------------------------------------
    browser = init_browser() 
    
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    
    time.sleep(1)
    
    html = browser.html
    
    soup = bs(html, 'html.parser')
    
    news_title = soup.find("div", class_="content_title").text
    
    news_p = soup.find("div", class_="article_teaser_body").text
    
    browser.quit()

    print(f'Title: {news_title}')
    print(f'Text: {news_p}')

    #-----Mars Facts-----------------------------------------
    
    facts_url = "https://space-facts.com/mars/"
    
    facts_table = pd.read_html(facts_url)
    
    df_mf = facts_table[0]
    
    df_mf.columns = ["Description", "Value"]
    
    df_mf.set_index("Description", inplace=True)
    
    mars_facts = df_mf.to_html(header= True, index=True)

    #--Mars Hemispheres

    browser = init_browser()


    usgs_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    html = browser.html

    usgs_soup = bs(html, "html.parser")

    main_url = "https://astrogeology.usgs.gov"


    spheres_url = usgs_soup.find_all("div", class_="item")

    marsh_url = []

    for sphere in spheres_url:
        mar_url = sphere.find('a')['href']
        marsh_url.append(mar_url)
    
    
    browser.quit()

    hemimg_url = []
    for mar in marsh_url:
        img_url = main_url + mar
        print(img_url)
        
        browser = init_browser()
        browser.visit(img_url)
    
        html = browser.html
    
        img_soup = bs(html, "html.parser")
    
        r_title = img_soup.find("h2", class_="title").text
    
        i_title = r_title.split (" Enhanced")[0]
    
        bimg_url = img_soup.find("li").a['href']
    
        hemimg_url.append({'title': i_title, 'img_url': bimg_url})
    
        browser.quit()

    print(hemimg_url)

    #------Mars Data Dictonary---------

    mars_data = {}
    
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_p
    mars_data["mars_facts"] = mars_facts
    mars_data["hemishperesimg_url"] = hemimg_url

    print("Scrape finished")

    return mars_data


