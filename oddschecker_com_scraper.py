import json
import datetime
import urllib.request
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 

URL_MAIN = "https://www.oddschecker.com/"
URL_FOOTBALL = URL_MAIN + "/football"

def parse_odds_by_betsite(line):
    link = URL_MAIN + line.find('a', href=True)['href']
    with urllib.request.urlopen(link) as page_x:
        html_page = page_x.read().decode('utf-8')
        content = BeautifulSoup(html_page, 'html5lib')
    table = content.find('table')
    websites = [w['title'] for w in table.find('tr', class_='eventTableHeader').findAll('a') if w['class'] != 'wo wo-col']
    data_t1, data_draw, data_t2 = table.find('tbody').findAll('tr')
    odds_t1 = [x.getText() for x in data_t1.findAll('td')[1:] if x['class'][0] != 'wo']
    odds_draw = [x.getText() for x in data_draw.findAll('td')[1:] if x['class'][0] != 'wo']
    odds_t2 = [x.getText() for x in data_t2.findAll('td')[1:] if x['class'][0] != 'wo']
    odds_sites = {}
    for site, win, draw, lose in zip(websites, odds_t1, odds_draw, odds_t2):
        odds_sites[site] =  {'win': win, 'draw': draw, 'lose':lose}
    return odds_sites

def parse_oddschecker_matchline(line):
    team1, team2 = (name.getText() for name in line.findAll('span', class_='fixtures-bet-name')
                if name.getText() != 'Draw')

    win, draw, lose = (odd.getText().strip() for odd in line.findAll('span', class_='odds'))

    extra_dict = parse_odds_by_betsite(line)
    #pp.pprint(extra_dict)
    return {'team1':team1, 
            'team2':team2,
            'aggregated_odds': {'win': win, 'draw': draw, 'lose': lose},
             **extra_dict}

def parse_oddschecker_table(table):
    lines = table.findAll('tr')
    date = None
    contents = []
    for line in lines[:3]:
        if line.findAll('td', class_='day slanted'):
            date = line.getText()
        try:
            classname = line.attrs['class']
            if 'date' in classname:
                date = line.getText()
            elif 'match-on' in classname:
                content = parse_oddschecker_matchline(line)
                content['match_date'] = date
                content['parsed_at_date'] = datetime.datetime.today().strftime("%A %d %B %Y")
                content['parsed_at_time'] = datetime.datetime.today().strftime("%H-%m-%S")
                contents.append(content)
        except KeyError:
            pass
    return contents

if __name__ == "__main__":
    print("Starting...")
    with urllib.request.urlopen(URL_FOOTBALL) as page_foot:
        html_page = page_foot.read().decode("utf-8")
        content = BeautifulSoup(html_page, "html5lib")

    with urllib.request.urlopen(URL_FOOTBALL) as page_foot:
        html_page = page_foot.read().decode("utf-8")
        content = BeautifulSoup(html_page, "html5lib")
        table = content.find('table')
        to_add = parse_oddschecker_table(table)
        ajourhui = datetime.datetime.today().strftime("date=%Y-%m-%d_time=%Hh-%Mm")
        print(ajourhui)
        with open('scrape_export_{today}.json'.format(today=ajourhui), 'w') as f:
            json.dump(to_add, f)
    print("Fin")
