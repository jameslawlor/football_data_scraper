import json
from datetime import datetime, timedelta
import urllib.request
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 

URL_MAIN = "https://www.sportinglife.com/"
URL_FOOTBALL = URL_MAIN + "football/fixtures-results"

def get_today(url_to_crawl):
    ...

def parse_table(date=None):
    if date:
        url_to_crawl = URL_FOOTBALL + date.strftime("/%Y-%M-%d")
    else:
        return get_today(URL_FOOTBALL)
    print(url_to_crawl)
    with urllib.request.urlopen(url_to_crawl) as page_results:
        html_page = page_results.read().decode("utf-8")
        content = BeautifulSoup(html_page, "html5lib")
        #print(content.find('div', class_='').prettify())


if __name__ == '__main__':
    print('Starting...')
    for i in range(1, 2):
        t = datetime.today() - timedelta(days=i)
        parse_table(date=t)
