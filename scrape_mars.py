from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
import os


def init_browser():
    CHROMEDRIVER_PATH = os.environ["CHROMEDRIVER_PATH"]
    executable_path = {'executable_path': CHROMEDRIVER_PATH}
    browser = Browser('chrome', **executable_path, headless=False)
    print('browser is ready')
    return browser


def scrape():
    mars_info = {}
    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find_all(attrs={'class': 'content_title'})[1].get_text()
    news_p = soup.find_all(attrs={'class': 'article_teaser_body'})[0].get_text()
    mars_info['news_title'] = news_title
    mars_info['news_text'] = news_p
    print(mars_info)

    # JPL Mars Space Images - Featured Image
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    browser.find_by_css('a#full_image.button.fancybox').first.click()
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_image = soup.find_all(attrs={'class': 'fancybox-image'})[0]
    url_image = mars_image.get('src')
    featured_image_url = 'https://www.jpl.nasa.gov/' + url_image
    mars_info['mars_url'] = featured_image_url
    print(mars_info)

    mars_info['mars_weather'] = "InSight sol 561 low -89.7ºC (-129.5ºF) high -2.9ºC (26.8ºF)\nwinds from the W at 5.7 m/s (12.8 mph) gusting to 17.8 m/s (39.8 mph)\npressure at 7.60 hPa"
    print(mars_info)


    # Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_url)[0]
    mars_table = mars_table.rename(columns={0: 'Value', 1: 'Description'})
    mars_table = mars_table.set_index('Description')
    mars_data = mars_table.to_html(classes='mars_data', justify='left')
    mars_info['mars_facts'] = mars_data
    print(mars_info)

    # Mars Hemispheres
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    hemisphere_image_urls = []
    for i in range(len(browser.find_by_css('img.thumb'))):
        img_page = browser.find_by_css('img.thumb')
        img_page[i].click()
        time.sleep(2)
        html = browser.html
        soup = bs(html, "html.parser")
        image_info = soup.find_all(attrs={'class': 'wide-image'})[0].get('src')
        title_info = soup.find_all("h2", attrs={'class': 'title'})[0].get_text()
        dict_info = {"title": title_info, "img_url": 'https://astrogeology.usgs.gov' + image_info}
        hemisphere_image_urls.append(dict_info)
        browser.back()

    mars_info['mars_images_titles'] = hemisphere_image_urls
    print(mars_info)

    browser.quit()

    return mars_info


if __name__ == "__main__":
    scrape()
