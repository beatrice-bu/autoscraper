from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import argh
import json
import os
import pandas as pd
import numpy as np


@argh.arg('websites', help='Path to .json file with websites to scrape. Required.')
@argh.arg('--path', '-p', help='Path to CHROME WEBDRIVER Selenium will use. Default is current folder.')
@argh.arg('--output', '-o', help='Path to OUTPUT folder where images will go. Default is current folder.')
@argh.arg('--scrolls', '-s', help="Define number of times autoscraper scrolls on a page. Default is 1.")
@argh.arg('--mode', '-m', choices=['csv','download'], help='Mode for downloading images. "csv" to download image data as a csv, "download" to download locally.')
def autoscrape(websites, output='output', path='./chromedriver.exe', scrolls=1, mode='csv'):
    import_mode = mode
    '''
    <WEBSITES JSON> <PATH TO OUTPUT FOLDER> <PATH TO CHROME WEBDRIVER> <# OF SCROLLS PER PAGE>
    Please be sure to download the Chrome Webdriver for whatever version of chrome you use. Can be found here: https://chromedriver.chromium.org/downloads
    
    
    '''
    #seperate doc strings as the docstring above is for argh -h 
    
    '''
    The next following commands are for masking our web scraper user agent as legitimate, as some websites will give 403 Forbidden errors to connections
    they believe are bots/spiders.
    
    Options is referring to the user-agent mask for Selenium's Webdriver
    opener is referring to the user-agent mask for urllib.
    '''
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    
    #these exceptions occasionally happen and are not fatal, so there is no need to let them stop our code
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    
    
    
    '''
    opening the path for `websites`, which is the .json file with our target websites and the file names associated with those websites. The json is saved as a dict
    with-as is used so that if there is an error at any step in the .json to dict process, the file will not stay open forever.
    '''
    with open(websites) as websites_json:
        websites_dict = json.load(websites_json)
        print(type(websites_dict))
    
    #creating the output directory file if it doesnt exist
    if not os.path.exists(output):
        os.makedirs(output)
    
    #list of URLS to each image, which will be retrieved by urllib
    image_sources = []
    image_texts = []
    image_sites = []
    #instantiating our selenium webdriver, using our path to chromedriver.exe and our new user-agent mask
    driver = webdriver.Chrome(path, options=options)
    
    #for each website and it's associated name in the websites_dict dictionary 
    for website, name in websites_dict.items():
        
        print(f'Scraping images from... {website}.')
        print(f'Saving images as... {name}.jpg')
        
        #open the website
        driver.get(website)
        
        '''
        use this to find our user-agent mask
        agent = driver.execute_script("return navigator.userAgent")
        print(agent)
        '''
        #scrolling down as many times as we specified. PAGE_DOWN is the most efficent way to do this and still load all images
        for scroll in range(scrolls):
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.PAGE_DOWN)
            #sleep for 2 seconds to let the webdriver download all images within view into memory
            time.sleep(2)
        try:
            
            try:
                #standard selenium method for waiting. Waits until all images are located on the website, or 15 seconds
                #whichever is sooner.
                element = WebDriverWait(driver, 15, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
                )
                
            finally:
                #saving a list of the locations of images on the page
                all_present_images = driver.find_elements_by_tag_name('img')
                #iterating through every image within all_present_images
                index = 0
                
                for image in all_present_images:
                    #acquiring the 'source' url of the image
                    image_source = image.get_attribute("src")
                    image_text = image.get_attribute("alt")
                    
                    
                    image_sources.append(image_source)
                    image_texts.append(image_text)
                    image_sites.append(name)
                    
                #now that we have all the image sources saved, we can close the page
                driver.close()
        finally:
            
            data = {
                        "source":image_sources,
                        "text":image_texts,
                        "site":image_sites
                    }
            df = pd.DataFrame.from_dict(data, dtype='str')
                
            if import_mode == 'csv':

                df.to_csv(output + '/' + 'image_data.csv', index=False)
                
            elif import_mode == 'download':
                
                img_num = 00
                for source in df['source']:
                    
                    # example: '/' + 'github' + '00' + .jpg' = '/github00.jpg'
                    file_name = "/" + name + str(img_num) + ".jpg"
                    #creates a variable that is the complete path of output folder + image name
                    image_location = output + file_name
                    #downloads the image to the selected location, from the iterated `image` source
                    urllib.request.urlretrieve(source, image_location)
                    img_num += 1
        driver.quit()



if __name__ == '__main__':
    argh.dispatch_command(autoscrape)
    


