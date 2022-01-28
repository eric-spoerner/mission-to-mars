from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) #Headless determines whether the browser will be open/observable for the scraping operation

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

# Scrape the news site
def mars_news(browser):
    url = 'http://redplanetscience.com'
    browser.visit(url)
    #optional delay for loading the page.  looks for tag/attrib combo and waits before query to ensure full page loads first
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Scrape the space image site
def featured_image(browser):
    url = 'http://spaceimages-mars.com'
    browser.visit(url)

    # Find by tag is a different way to dig up tags!  neat.
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse this page
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # grab relative url of first image
    try:
        img_url_rel = img_soup.find('img', class_="fancybox-image").get("src")
    except AttributeError:
        return None

    img_url = f'{url}/{img_url_rel}'

    return img_url

# Read fact table using pandas read_html()
def mars_facts(browser):
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html()

if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())