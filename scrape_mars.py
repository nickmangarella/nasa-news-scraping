# Dependencies and Setup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def scrape():

    # Setup splinter
    executable_path = {"executable_path": "C:\webdrivers\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Website to open in chrome
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Iterate through the first news page
    for x in range(1):

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
    
        # Scrape the latest news title and paragraph text
        news_title = soup.find_all('div', class_='content_title')[1].text
        news_p = soup.find_all('div', class_='article_teaser_body')[0].text


    # Website to open in chrome
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the featured image
    image_path = soup.find_all('img')[1]['src']

    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_path

    # URL to read with Pandas
    url = 'https://space-facts.com/mars/'

    # Scrape the table with facts about Mars
    tables = pd.read_html(url)

    # Save the first table as DataFrame
    df = tables[0]

    # Add 'Description' to first row
    row = pd.DataFrame({0: 'Description', 1: ''}, index=[0])
    df = pd.concat([row, df]).reset_index(drop = True)

    # Rename columns
    df.rename(columns={0: '', 1: 'Mars'}, inplace=True)

    # Convert the DataFrame to an HTML table string
    mars_table = df.to_html()

    # Website to open in chrome
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve each link to the hemispheres pages
    hemispheres = soup.find_all('div', class_='item')

    hemisphere_links = []
    hemisphere_image_urls = []
    # Iterate through each hemisphere
    for x in hemispheres:
    
        # Append each hemisphere link to a list
        base_url = 'https://astrogeology.usgs.gov'
        hemisphere_links.append(url + x.find('a')['href'])
    
    # Iterate through each hemisphere link
    for x in hemisphere_links:
    
        # Websites to open in chrome
        browser.visit(x)
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape the hemisphere title and image url
        title = soup.find('h2', class_='title').text
        img_url = base_url + soup.find('img', class_='wide-image')['src']
                            
        # Append each dictionary with the hemisphere title and image url to a list
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    
    # Store the data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_table': mars_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # Return the results
    return mars_data