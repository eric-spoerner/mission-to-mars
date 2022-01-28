from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pprint import pprint

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Scrape the news site

url = 'http://redplanetscience.com'
browser.visit(url)
#optional delay for loading the page.  looks for tag/attrib combo and waits before query to ensure full page loads first
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# Scrape the space image site

url = 'http://spaceimages-mars.com'
browser.visit(url)

# Find by tag is a different way to dig up tags!  neat.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse this page
html = browser.html
img_soup = soup(html, 'html.parser')

# grab relative url of first image
img_url_rel = img_soup.find('img', class_="fancybox-image").get("src")
img_url = f'{url}/{img_url_rel}'

# Read fact table using pandas read_html()
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
pprint(df)

# convert table back to html
pprint(df.to_html())

# close the durn session!
browser.quit()

