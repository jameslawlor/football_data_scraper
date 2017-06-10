import json
from datetime import datetime, timedelta
import urllib.request
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 

URL_MAIN = "https://www.sportinglife.com/"
URL_FOOTBALL = URL_MAIN + "football/fixtures-results"

def print_json(match_dict):
    title = 'match_result_date={}_{}_v_{}.json'.format(
                match_dict['date'],
                match_dict['teamA'],
                match_dict['teamB'])
    with open(title, 'w') as f:
        json.dump(match_dict, f)

def parse_category(category_table, date):
    #print(category_table.prettify())
    date_str = date.strftime("%Y-%m-%d")
    cat_title = category_table.find('h2', class_="sectionTitle").getText()
    matches = category_table.findAll('div', class_="footballMatchListItem")
    for match in matches[:]:
        teamA = match.find('div', class_='teamA').getText()
        teamB = match.find('div', class_='teamB').getText()
        score = match.find('div', class_='scoreString matchNotStartedOrFullTime').getText()
        try:
            goalA, goalB = (int(pts.strip()) for pts in score.split('-'))
        except ValueError:
            goalA, goalB = float('NaN'), float('NaN')

        match_result = {'teamA'          : teamA,
                        'teamB'          : teamB,
                        'goalsA'         : goalA,
                        'goalsB'         : goalB,
                        'match category' : cat_title,
                        'date'           : date_str}

        print_json(match_result)

def parse_table(date):
    url_to_crawl = URL_FOOTBALL + date.strftime("/%Y-%m-%d")
    print(url_to_crawl)
    with urllib.request.urlopen(url_to_crawl) as page_results:
        html_page = page_results.read().decode("utf-8")
        content = BeautifulSoup(html_page, "html5lib")
        match_cats = content.find('div', class_="footballFixturesResults").findAll('div', class_="FootballMatchList")
        for match_category in match_cats[:]:
            parse_category(match_category, date)



if __name__ == '__main__':
    print('Starting...')
    for i in range(1, 2):
        t = datetime.today() - timedelta(days=i)
        parse_table(date=t)
