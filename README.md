## Web_scraping_MongoDB
### Here I used Splinter and BeautifulSoup to scape news information and images from the following sources
<br />
<li>Nasa Mars News site : https://mars.nasa.gov/news/ (most recent headline)</li>
<li>JPL Mars Space Images  : https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars (get the featured image)</li>
<li>Mars Weather : https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars (get updated weather tweets)</li>
<li>Mars Facts: http://space-facts.com/mars/ (use PANDAS to scrape the Mars facts table)</li>
<li>Mars Hemispheres: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars (get 4 hemisphere images)</li>

### Then I stored the scraped news into MongoDB and used Flask Application to create a html to scrape and render this information</br>
<br />
<p>Click the scrape button on the website will scrape information from the news source listed above</p>
<p>but the scraping take some time so please be patient</p>
<br />

### Following scripts are found in the repo
<li><a href="https://github.com/yizhiyin86/Web_scraping_MongoDB/blob/master/scrape_mars.py">1. scrape_mars.py (script to scrape information)</a></li>
<li>2. app.py (Flask app.py to render)</li>
<li>3. templates/index.html (rendering html)</li>
<li>4. mission_to_mars.ipynb (jupyter notebook script I used for troubleshooting scrape_mars.py)</li>
<li>5. two jpg images to show one scraping of the website</li>

### Below is a jpg of the final html 
![Mars html](Mars_webpage_1.jpg?raw=true "Mars webpage 1")
![Mars html](Mars_webpage_2.jpg?raw=true "Mars webpage 2")




