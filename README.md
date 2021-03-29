# NASA-News-Scraping

## Description
Implementing BeautifulSoup, Pandas, splinter, and Flask modules with MongoDB to deploy a web application that scrapes various websites for data relatd to the NASA Mission to Mars and displays this data on an HTML page.

## Scraping
First used Jupyter Notebook to scrape all the following information without error before copying to "scrape_mars.py"

### "scrape_mars.py"
* Created a function "init_browser()" with splinter to open a chrome browser for urls to be scraped

    def init_browser():
    
        executable_path = {"executable_path": "C:\webdrivers\chromedriver.exe"}
        return Browser("chrome", **executable_path, headless=False)

* Created another function "scrape()" that called the urls to be scraped and BeautifulSoup/Pandas to scrape the data from each url and return that data in a dictionary

    def scrape():

        browser = init_browser()

        # Website to open in chrome
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # Store the data in a dictionary
        mars_data = {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'mars_table': mars_table,
            'hemisphere_image_urls': hemisphere_image_urls
        }

        .....

        # Return the results
        return mars_data

## Scraped Data

### Nasa Mars News
* Used splinter and chromedriver to scrape (https://mars.nasa.gov/news/) and collect the latest news title and the paragraph text

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


### JPL Mars Space Images - Featured Image
* Used slinter and chromedriver to scrape (https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html) and capture the site's "featured image" url

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

### Mars Facts
* Used Pandas to scrape (https://space-facts.com/mars/) and convert the first table containing the facts about the planet to an HTML table string

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
        mars_table = df.to_html(classes="table table-striped")

### Mars Hemisphere's
* Used splinter and chromedriver to scrape (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) and gather the urls to the high resolution images of Mars's four hemispheres
* Involved looping through each url to the indiviual hemisphere pages and capturing the high resolution image there

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
            url = 'https://astrogeology.usgs.gov'
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
            img_url = url + soup.find('img', class_='wide-image')['src']
                                    
            # Append each dictionary with the hemisphere title and image url to a list
            hemisphere_image_urls.append({'title': title, 'img_url': img_url})

## MongoDB and Flask App
Created "app.py" that called the scraped data from "scrape_mars.py" and stored it in MongoDB to then display on an HTML page

### "app.py"
* Created an instance of Flask and connection to Mongo using PyMongo

        app = Flask(__name__)
        mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

        if __name__ == '__main__':
        app.run(debug=True)

* Made a route to the HTML page to connect to MongoDB and render the data on the webpage

        @app.route('/')
        def home():

            # Find one record of data from the mongo database
            planet = mongo.db.collection.find_one()

            # Reutrn template and data
            return render_template('index.html', mars=planet)

* Created a route to the "scrape_mars.py" file to intialize the scraping of the data and store in MongoDB 

        @app.route('/scrape')
        def scrape():

            # Run the scrape funciton
            mars_data = scrape_mars.scrape()

            # Update the Mongo database using update and upsert=True
            mongo.db.collection.update({}, mars_data, upsert=True)

            # Redirect back to home page
            return redirect('/')






