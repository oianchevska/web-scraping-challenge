from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # executable_path = {'executable_path': '/app/chromedriver1'}
    # print(executable_path)
    # return Browser('chrome', **executable_path, headless=False)
    # GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome-stable'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    # CHROMEDRIVER_PATH='./Missions_to_Mars/chromedriver'
    # chrome_options = webdriver.ChromeOptions()
    #
    # chrome_options.binary_location = GOOGLE_CHROME_PATH
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('headless')
    #
    # browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

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
    browser.quit()

    browser = init_browser()
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
    browser.quit()

    browser = init_browser()
    # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    browser.reload()
    time.sleep(5)
    html = browser.html
    print(html)
    soup = bs(html, "html.parser")
    print(soup)
    twitter_news = soup.find_all(attrs={'role': 'article'})[0]
    mars_weather = twitter_news.find(attrs={'lang': 'en'}).get_text()

    mars_info['mars_weather'] = mars_weather
    print(mars_info)
    browser.quit()

    browser = init_browser()
    # Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_url)[0]
    mars_table = mars_table.rename(columns={0: 'Value', 1: 'Description'})
    mars_table = mars_table.set_index('Description')
    mars_data = mars_table.to_html(classes='mars_data', justify='left')

    mars_info['mars_facts'] = mars_data
    print(mars_info)
    browser.quit()

    browser = init_browser()
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
