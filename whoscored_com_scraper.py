import json
import datetime
import urllib.request
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 
import selenium
from selenium import webdriver

#USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
USER_AGENT = "FriendlyCrawler (pls don't ban)"
HEADERS = {'User-Agent': USER_AGENT}
URL_MAIN = "https://fr.whoscored.com/Statistics"

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.whoscored.com/Statistics")
    html = driver.page_source
    driver.close()
    print(html)
