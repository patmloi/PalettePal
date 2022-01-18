# Import statements
# Webdriver
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from PIL import Image
from io import BytesIO

import time
import requests

from typing import Union, Literal, Tuple, List, Any

def startDriver() -> webdriver.Chrome:
    # GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    # CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument("--headless")

    

    # chromeOptions.binary_location = GOOGLE_CHROME_PATH # CHROMEDRIVER_PATH
    driver = webdriver.Chrome(chrome_options=chromeOptions) # ChromeDriverManager().install(), chrome_options=chromeOptions)
    print("Driver")
    return driver

def loadPage(wd: webdriver.Chrome, searchTerm: str):
    '''First loads the search results page.'''
    searchUrl = "https://www.google.com/search?safe=on&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(searchUrl.format(q=searchTerm))

def scrollEnd(wd: webdriver.Chrome):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def loadMore(wd: webdriver.Chrome):
    ''' Finds and clicks on the "Load More" button.'''
    isButton= wd.find_elements(By.CSS_SELECTOR, ".mye4qd")
    if  isButton:
        wd.execute_script("document.querySelector('.mye4qd').click();")
    
def getThumbnailResults(wd: webdriver.Chrome) -> Tuple[list, int]:
    thumbnailResults= wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    resultNo = len(thumbnailResults)
    print("Thumbnail Results")
    return thumbnailResults, resultNo

def getImageUrl(wd: webdriver.Chrome) -> Union[str, Literal[False]]:
    '''Gets the source URL from a clicked image and appends it to imageUrls.'''

    actualImages = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
    for am in actualImages:
        if am.get_attribute('src') and 'http' in am.get_attribute('src'):
            imageUrl = am.get_attribute('src')
            return imageUrl

    return False

def getImageContent(url: str) -> Union[bytes, Literal[False]]:
    # Get image content
    try:
        imageContent = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        imageContent = False

    return imageContent

def openImage(url: str): # -> Union["PIL.Image", Literal[None]]
    # Get image content 
    imageContent = getImageContent(url)
    
    # Download image content
    if imageContent != False:
        try:
            img = Image.open(BytesIO(imageContent))
            return img
        except Exception as e:
            print(f"ERROR")

    return False

def _getImages(searchTerm: str, imageNo: int, wd: webdriver.Chrome) -> List[Any]: # PIL
    loadPage(wd, searchTerm)

    images = []
    imageUrls = []
    imageCount = 0
    resultStart = 0

    while imageCount < imageNo:
        # Loading results from first page
        scrollEnd(wd)
        thumbnailResults, resultNo = getThumbnailResults(wd)

        cont = True
        for img in thumbnailResults[resultStart:resultNo]:
            # Try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
            except Exception:
                continue
            
            resultStart += 1

            imageUrl = getImageUrl(wd)
            print(f"URL No. {resultStart, imageUrl}")

            if imageUrl == False:
                continue

            print(f"Valid URL No. {resultStart}")
            
            
            image = openImage(imageUrl)
            print(f"Image No. {resultStart}")

            if image == False:
                continue

            print(f"Valid Image No. {resultStart}")

            images.append(image)
            imageUrls.append(imageUrl)

            imageCount += 1
            print(f"Image Count: {imageCount}")

            if imageCount >= imageNo: 
                cont = False
                break
    
        if not cont: # Prevent duplication of conditional when it is costly
            break

        else:
            loadMore(wd)
    
    return images, imageUrls

def getImages(searchTerm: str, imageNo: int) -> list:
    wd = startDriver()
    images, imageUrls = _getImages(searchTerm, imageNo, wd)

    wd.close()
    return images, imageUrls




