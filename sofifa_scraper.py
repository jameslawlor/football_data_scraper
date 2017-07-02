import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 
import os
import numpy as np
from collections import OrderedDict
import time

#URL_MAIN = 'https://sofifa.com/'
URL_MAIN = 'https://fifaindex.com'
LEAGUE_IDS_FILE = 'fifaindex_league_ids.json'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)  \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape_league_ids():
    """
    Scrapes all League names and their ids from fifaindex.com
    """

    with requests.Session() as s:
        s.headers.update(headers)
        url = URL_MAIN + "/teams"
        
        download = s.get(url)
        decoded_content = download.text
        soup = BeautifulSoup(decoded_content, 'html5lib')
        form = soup.find('select',id='id_league')
        #print(form)
        options = form.findAll('option')
        league_id_dic = {}
        for option in options:
            url_id = str(option['value']) 
            league = str(option.get_text())
            league_id_dic[league] = url_id
    
        with open(f_league_ids,'w') as outfile:
            json.dump(league_id_dic, outfile)
        
        print("Data scraped, waiting....")
        time.sleep(np.random.uniform(low=5.0, high=15.0, size=None))

def scrape_team_ids(_league, _url):
    """
    For a league at _url, scrape all team names and their hyperlinks,
    return dictionary of these to main
    """
    team_url_dic = {}

    with requests.Session() as s:
        s.headers.update(headers)
        download = s.get(_url)
        decoded_content = download.text
        soup = BeautifulSoup(decoded_content, 'html5lib')
        tds = soup.find_all("td",colspan="2")
        for td in tds:
            link = td.find('a').get('href')
            team_name = td.find('a').get('title')
            print(link, team_name)
            team_url_dic[team_name] = link

    print("Team IDs and Hyperlinks scraped for {}. Pausing....".format(_league))
    time.sleep(np.random.uniform(low=5.0, high=15.0, size=None))
    return team_url_dic

def scrape_player_ids(_team_url):
    """
    For a team at _team_url, get all their players and hyperlinks
    """
    
    player_url_dic = {}
    with requests.Session() as s:
        s.headers.update(headers)
        print(_team_url_)
        stop
        download = s.get(_team_url)
        decoded_content = download.text
        soup = BeautifulSoup(decoded_content, 'html5lib')
        tds = soup.find_all("td",colspan="2")
        for td in tds:
            link = td.find('a').get('href')
            team_name = td.find('a').get('title')
            print(link, team_name)
            team_url_dic[team_name] = link

    print("Team IDs and Hyperlinks scraped for {}. Pausing....".format(_league))
    time.sleep(np.random.uniform(low=1.0, high=10.0, size=None))

    return player_url_dic

def load_team_ids(_name, _url):

    team_ids_file = _name + ".json"

    if not os.path.isfile(team_ids_file):
        print("Data not found for {}, scraping...".format(_name))
        league_base_url = URL_MAIN + _url
        url_to_scrape = league_base_url.format(_id)
        team_ids_dic = scrape_team_ids(_name, url_to_scrape)
        print(team_ids_dic)
        with open(team_ids_file,'w') as outfile:
            print(outfile)
            json.dump(dic, outfile)

    else:
        with open(team_ids_file ,"r") as data_dic:
            dic = json.load(data_dic)

    return dic

def get_players(_url_extension):

    url = URL_MAIN + "/{}".format(_url_extension)

if __name__ == '__main__':

    print('Starting...')
    
    if not os.path.isfile(LEAGUE_IDS_FILE):
        print('League IDs not found, scraping...')
        scrape_league_ids()

    with open(LEAGUE_IDS_FILE) as data_dic:    
        league_ids = json.load(data_dic)
   
    test_id = "13"
    league_ids = [(k,v) for k,v in league_ids.items() if v == test_id]

    for league_name, league_id in league_ids:
        print("Loading data for {}".format(league_name))
        team_ids_dic = load_team_ids(league_name,league_id)
        for team, url in team_ids_dic.items():
            print(team, url)
            load_team_ids(team,url)
                    
            stop
