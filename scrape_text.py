from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import html2text
import time
from bs4 import BeautifulSoup
import os

def setWebdriver():
    firefox_service = FirefoxService(executable_path="/Users/apple/opt/anaconda3/lib/python3.8/site-packages/selenium/webdriver/geckodriver")
    firefox_options = Options()
    firefox_options.headless = False  # Run Firefox in headless mode (no GUI)
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    return driver

def load_page(url, driver):
    
    driver.get(url)

    time.sleep(10)
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

def getPageContent(url, driver):

    load_page(url, driver)

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    article_class = "slds-col--padded slds-size--12-of-12 slds-medium-size--6-of-12 slds-medium-order--2 slds-large-size--6-of-12 slds-large-order--2 comm-layout-column"
    article = soup.find(class_ = article_class)

    return str(article)


def get_scraped_text(driver, url, foldername = None, filename = None, article_content = None):

    article = getPageContent(url, driver)

    # Create an instance of the html2text converter
    h = html2text.HTML2Text()
    h.ignore_links = False  # Preserve links in the converted text

    # Convert HTML to formatted text while preserving links
    formatted_text = h.handle(article)
    
    # Save the formatted text to a file or process it as needed  
    filename = filename + '.txt'
    filename = filename.replace('/', '_or_')
    path = 'knowledge_base/' + foldername

    # Check if the folder exists
    if not os.path.exists(path):
        os.makedirs(path)
    
    try: 
        with open(path + '/' + filename, 'w') as file:
            file.write(formatted_text)
    except Exception as e:
        print(f"An error occurred while exporting txt file: {str(e)} \n ***** Process resumed *****")
    
    # return text
    return formatted_text


if __name__ == '__main__':
    driver = setWebdriver()
    url = ''
    text = get_scraped_text(driver, url)
    print(text)