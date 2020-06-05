from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

    
    # MARS NEWS 
def title_p(browser):
    
    # Visit vpage for latest mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #wait
    time.sleep(1)

    # scrape page into Soup
    nasa_html = browser.html
    time.sleep(1)
    nasa_soup = bs(nasa_html, "html.parser")
    
    #get NASA news title
    news_title = nasa_soup.select_one('.item_list div.bottom_gradient').text
    
    #get NASA news article preview
    news_preview = nasa_soup.select_one('.list_text').find('div', class_='article_teaser_body').get_text()
    
    return news_title, news_preview

### JPL Mars Space Images - Featured Image
def JPL(browser):
    #visit NASA jpl 
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    # Interact with elements
    browser.links.find_by_partial_text('more info').click()
    time.sleep(3)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    lede = jpl_soup.select_one('figure.lede')
    #  browser.is_element_present_by_css('figure.lede', wait_time=2)
    part_2 = lede.find('img')['src']
    featured_image_url = f"https://www.jpl.nasa.gov{part_2}"
    
    return featured_image_url

# Visit Twitter Weather
def weather(browser):
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(4)

    twitter_html = browser.html
    
    twitter_soup = bs(twitter_html, 'html.parser')
    time.sleep(2)
    regex = re.compile(r'InSight')
    weather_regex = twitter_soup.find('span', text=regex).get_text()
    ##use regex to remove newline
    mars_weather = weather_regex.replace('\n', '')

    return mars_weather

# Visit Mars Facts  Webpage
def mfacts(browser):
    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)
 
    mar_facts_df = facts[0]
    mar_facts_df = pd.DataFrame(mar_facts_df)
    mar_facts_df.rename(columns={0:'', 1:'value'}, inplace=True)
    mar_facts_df.set_index('', inplace=True)
    mars_facts = mar_facts_df.to_html()
    

    return mars_facts

# Mars Hemispheres
def hemispheres_url(browser):
    spheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(spheres_url)

    hemispheres = []
    hemis = browser.find_by_css('a.itemLink img.thumb')
    for i in range(len(hemis)):
        img_link= {}
        time.sleep(1)
        hemis[i].click()
        img_url = browser.links.find_by_text('Sample').first['href']
        img_link['img_url'] = img_url
        title = browser.title.replace(' | USGS Astrogeology Science Center', '')
        img_link['title'] = title
        hemispheres.append(img_link)    
        browser.back()
        hemis = browser.find_by_css('a.itemLink img.thumb')
        

        
    return hemispheres

def final_info():
    browser = init_browser()
    news_title, news_preview = title_p(browser)
    featured_image_url = JPL(browser)
    mars_weather = weather(browser)
    mars_facts = mfacts(browser)
    hemispheres = hemispheres_url(browser)


    mars_data = {
        "news_title": news_title,
        "news_preview": news_preview,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemispheres": hemispheres
    }

    browser.quit()
    # Return results
    return mars_data


if __name__ == "__main__":
    print(final_info())
