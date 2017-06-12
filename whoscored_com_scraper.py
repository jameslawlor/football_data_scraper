import json
import datetime
import urllib.request
import re
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 
import selenium
from selenium import webdriver

#USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
USER_AGENT = "FriendlyCrawler (pls don't ban)"
HEADERS = {'User-Agent': USER_AGENT}
URL_MAIN = "https://fr.whoscored.com/Statistics"

def get_number_pages(bs4_html):
    txt = bs4_html.find('dl', class_="listbox right").getText()
    # Regex gets the digit after " Page 1/"
    target = re.search(r"(?<=\s\w{4}\s\d/)\d", txt)
    n = int(target.group(0))
    return n

def get_summary(driver, num_pages: int):
    html = BeautifulSoup(driver.page_source, "html5lib")
    res_table = html.find('div', attrs={'id':'statistics-team-table-summary'})
    {}
    for _ in range(num_pages):
        pass

    return _

if __name__ == "__main__":
    driver = webdriver.Firefox()
    # wrapping in try/finally as to make sure the browser gets closed no matter what
    try:
        driver.get("https://www.whoscored.com/Statistics")
        print("done getting")
        html = BeautifulSoup(driver.page_source, "html5lib")
        num_pages = get_number_pages(html)
        print("number pages = {}".format(num_pages))
        get_summary(driver, num_pages)
    finally:
        driver.close()
    print("Done")
