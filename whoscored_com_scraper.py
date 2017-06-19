import json
import datetime
import urllib.request
import re
from bs4 import BeautifulSoup
from pprint import PrettyPrinter 
import selenium
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep

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

def click_next(driver: webdriver):
    try:
        next_button = driver.find_element_by_id('next')
        next_button.click()
        sleep(5)
    except ElementNotInteractableException:
        next_buttons = driver.find_elements_by_xpath("//a[@id='next']")
        next_buttons[1].click()
        sleep(5)



def parse_table_summary(driver, num_pages, tag='overall'):

    result = []
    for i in range(num_pages):
        # Don't click 'next' if you're on the first page
        if i:
            click_next(driver)

        html = BeautifulSoup(driver.page_source, "html5lib")
        table_html = html.find('div', attrs={'id':'statistics-team-table-summary'})
        team_names = table_html.findAll('td', class_='tn')
        tournaments = table_html.findAll('td', class_='tournament')
        shots_per_game = table_html.findAll('td', class_='shotsPerGame ')
        cards = table_html.findAll('td', class_='aaa')
        possession = table_html.findAll('td', class_='possession ')
        passSuccess = table_html.findAll('td', class_='passSuccess ')
        aerialsWon = table_html.findAll('td', class_='aerialWonPerGame ')
        rating = table_html.findAll('td', class_=' sorted ')
        page_summary = []
        for tn, trn, spg, c, pos, passOK, aer, rt in zip(team_names, tournaments, shots_per_game, cards, possession, passSuccess, aerialsWon, rating):
            page_summary.append({'team-name': tn.getText(),
                                'tournament': trn.getText(),
                                'shots-per-game-{}'.format(tag): spg.getText(),
                                'cards-{}'.format(tag): c.getText(),
                                'possession-{}'.format(tag): pos.getText(),
                                'successful-passes-{}'.format(tag): passOK.getText(),
                                'aerials-won-{}'.format(tag): aer.getText(),
                                'rating': rt.getText()})
        result.extend(page_summary)
    return result

def get_summary(driver, num_pages: int):
    sleep(5)
    pp = PrettyPrinter()

    # Get overall stats
    res1 = parse_table_summary(driver, num_pages, tag='overall')

    ## Get stats for home games
    element = driver.find_element_by_link_text('Home')
    element.click()
    sleep(5)
    res2 = parse_table_summary(driver, num_pages, tag='home')

    ## Get stats for away games
    element = driver.find_element_by_link_text('Away')
    element.click()
    sleep(5)
    res3 = parse_table_summary(driver, num_pages, tag='away')

    # Join results
    res_final = []
    for overall, home, away in zip(res1, res2, res3):
        stats = {**overall, **home, **away}
        res_final.append(stats)

    return res_final

def parse_table_defense(driver, num_pages, tag='overall'):
    pp = PrettyPrinter()

    result = []
    for i in range(num_pages):
        # Don't click 'next' if you're on the first page
        if i:
            click_next(driver)
        print('On page {}'.format(i+1))

        html = BeautifulSoup(driver.page_source, "html5lib")
        table_html = html.find('div', attrs={'id':'statistics-team-table-defensive'})
        # team_name, tournament, shotsPerGame, tacklePerGame, interceptionPerGame, foulsPerGame, offsideGivenPerGame, stat-value rating
        team_names = table_html.findAll('td', class_='tn')
        #print('team name', len(team_names))
        tournaments = table_html.findAll('td', class_='tournament')
        #print('tournament', len(tournaments))
        shotsPerGame = table_html.findAll('td', class_='shotsConcededPerGame ')
        #print('shots per game', len(shotsPerGame))
        tacklePerGame = table_html.findAll('td', class_='tacklePerGame sorted ')
        #print('tackle per game', len(tacklePerGame))
        interceptionPerGame = table_html.findAll('td', class_='interceptionPerGame ')
        #print('interception per game', len(interceptionPerGame))
        offsidesPerGame = table_html.findAll('td', class_='offsideGivenPerGame ')
        #print('offsides per game', len(offsidesPerGame))
        rating = table_html.findAll('span', class_='stat-value rating') 
        #print('rating', len(rating))
        page_summary = []
        for tn, trn, spg, tpg, ipg, opg, rt in zip(team_names, tournaments, shotsPerGame, tacklePerGame, interceptionPerGame, offsidesPerGame, rating):
            page_summary.append({'team-name': tn.getText(),
                                'tournament': trn.getText(),
                                'shots-per-game-{}'.format(tag): spg.getText(),
                                'tackles-per-game-{}'.format(tag): tpg.getText(),
                                'interceptions-per-game-{}'.format(tag): ipg.getText(),
                                'offsides-per-game-{}'.format(tag): opg.getText(),
                                'rating': rt.getText()})
        result.extend(page_summary)

    return result

def get_defense(driver, num_pages: int):
    pp = PrettyPrinter()
    element = driver.find_element_by_link_text('Defensive')
    element.click()
    sleep(5)

    # Get overall stats
    res1 = parse_table_defense(driver, num_pages, tag='overall')

    # Get stats for home games
    elements = driver.find_elements_by_link_text('Home')
    elements[1].click()
    sleep(5)
    res2 = parse_table_defense(driver, num_pages, tag='home')

    # Get stats for away games
    elements = driver.find_elements_by_link_text('Away')
    elements[1].click()
    sleep(5)
    res3 = parse_table_defense(driver, num_pages, tag='away')

    ## Join results
    res_final = []
    for overall, home, away in zip(res1, res2, res3):
        stats = {**overall, **home, **away}
        res_final.append(stats)
    pp.pprint(res_final)
    return res_final


def print_json(lst, tag):
    print('Here')
    ajourhui = datetime.datetime.today().strftime("date=%Y-%m-%d_time=%Hh-%Mm")
    with open('scrape_export_whoscored_com_{tag}_{today}.json'.format(today=ajourhui, tag=tag), 'w') as f:
        json.dump(lst, f)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    # wrapping in try/finally as to make sure the browser gets closed no matter what
    try:
        driver.get("https://www.whoscored.com/Statistics")
        html = BeautifulSoup(driver.page_source, "html5lib")
        num_pages = get_number_pages(html)
        #summary = get_summary(driver, num_pages)
        #print_json(summary, tag='summary')
        defense = get_defense(driver, num_pages)
        print_json(defense, tag='defensive')
    finally:
        driver.close()
        pass
    print("Done")
