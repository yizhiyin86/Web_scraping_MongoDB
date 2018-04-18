#import dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import re 
import pandas as pd

#helper function to get browser initiated
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#scraping function
#________________________________________________________________________________
#news source  (output_name/type)
# https://mars.nasa.gov/news/ (news_data/python dic)
#https://www.jpl.nasa.gov/spaceimages/?search=Mars&category=Featured (featured_image_url/text)
#https://twitter.com/marswxreport?lang=en (weather/text)
#https://space-facts.com/mars/ (facts/pd table)
#https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars (hemi_info/python list)
#_______________________________________________________________________________
def scrape():
    browser = init_browser()
    #create final dict to return
    result={}
    #_______________________________________________________________________
    #scrape from https://mars.nasa.gov/news/ 
    #_______________________________________________________________________
    # create news_data dict
    news_data = {}
    # visit mars.nasa.com
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(1)
    html = browser.html
    time.sleep(1)

    # create a soup object from the html
    news = BeautifulSoup(html, "html.parser")

    #get news title,text,and date as values in the news_data dict
    news_data['title']=news.find("div", class_="content_title").text
    print("debug title is {}\n".format(news_data['title']))

    news_data['content']=news.find("div", class_="article_teaser_body").text
    # print("debug title is {}\n".format(news_data['content']))

    news_data['time']=news.find("div",class_="list_date").text
    # print("debug title is {}\n".format(news_data['time']))

    #insert news_data into the result dict
    result['news_data']=news_data
    print('debug current result is {}/n'.format(result))
    #_______________________________________________________________________
    #scrape from https://www.jpl.nasa.gov/spaceimages/?search=Mars&category=Featured 
    #_______________________________________________________________________
    #get link and visit
    picture_link="https://www.jpl.nasa.gov/spaceimages/?search=Mars&category=Featured"
    browser.visit(picture_link)
    time.sleep(1)

    # The website has the featured_image with a button with the id "full_image" and click it 
    button = browser.find_by_id("full_image")
    button.click()
    time.sleep(1)
    html_pic = browser.html
    time.sleep(1)
    #pass it to another beautiful soup object
    image= BeautifulSoup(html_pic, "html.parser")

    #find the image src of the image
    #here the image src is just mediumsize
    image_src=image.find('img',class_='fancybox-image')['src']
    # print("debug here I am the src of the featured image {}".format(image_src))

    #I exhausted that webpage but really cannot find the large size image of the current image
    #I can find the next largesize image but not the current one
    #So I decided to extract the image ID and plugged it in the largesize image link

    image_id=re.findall('/[a-zA-Z0-9]+_',image_src)[0][1:-1]
    fullsize_link='https://www.jpl.nasa.gov/spaceimages/images/largesize/{}_hires.jpg'.format(image_id)
    # print('hey I am the fullsize image link {}'.format(fullsize_link))
    result['featured_image']=fullsize_link
    print('debug current result is {}'.format(result))

    #_______________________________________________________________________
    #scrape from https://twitter.com/marswxreport?lang=en 
    #get weather info
    #_______________________________________________________________________
    weather_link='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_link)
    time.sleep(1)
    html_weather=browser.html
    time.sleep(1)
    weather=BeautifulSoup(html_weather,'html.parser')
    current_weather=weather.find('div',class_='js-tweet-text-container').p.text
    # print('debug current weather in Marse is {}'.format(current_weather))
    result['weather']=current_weather
    print('debug current result is {}'.format(result))
    
    
    #_______________________________________________________________________
    #scrape from https://space-facts.com/mars/ 
    #get facts table
    #_______________________________________________________________________


    facts_url='https://space-facts.com/mars/'
    facts_table=pd.read_html(facts_url)[0]
    facts_table.columns=['Description','Value']
    facts_table=facts_table.set_index('Description')
    html_table = facts_table.to_html()
    #put it in the dict
    result['facts_table']=html_table
    print('debug the column of the table has been inserted {}/n'.format(html_table))

     #_______________________________________________________________________
    #scrape from https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars 
    #get hemisphere images and title
    #_______________________________________________________________________
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_image_urls=[]
    browser.visit(hemi_url)

    # The website has the featured_image with a button with the id "full_image" and click it 
    each_hemi_url = browser.find_by_css('div[class="description"] a')
    href_list=[i['href'] for i in each_hemi_url ]

    #enter for look to visit all the links to the final full image site
    for i in href_list:
        browser.visit(i)  #visit the full image url
        html=browser.html  #connect
        #pass it to a beautiful soup object
        final_html=BeautifulSoup(html,'html.parser')
        #get the relative path
        image_relative_path=final_html.find('img',class_='wide-image')['src']
        # print("debug hey my relative path is {}".format(image_relative_path))
        #get full link of the image
        image_full_link='https://astrogeology.usgs.gov{}'.format(image_relative_path)
        # print('debug hey my full path is {}'.format(image_full_link))
        #get image title
        image_title=final_html.find('h2',class_='title').text
        # print('debug hey my title is {}'.format(image_title))
        hemi_image_urls.append({"title":image_title,"image_url":image_full_link})
        # print('hey so far this is my list {}'.format(hemi_image_urls))
        time.sleep(2)   # sleep
        
    #put it in the news_data dict
    result['hemi_info']=hemi_image_urls
    print('debug hey hemi_info has been inserted {}/n'.format(result['hemi_info']))

    return result

# def report(scrape_result):
#     for key,value in scrape_result.items():
#         print(key,value)

# scrape_result=scrape()
# print("hey final final result is {}".format(scrape_result))






