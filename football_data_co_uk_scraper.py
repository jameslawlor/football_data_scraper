"""
Scrapes CSV data from football-data.co.uk
"""

import requests
import csv
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

data_path = "./data/"
url_template = "http://football-data.co.uk/mmz4281/{season}/{league}.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Pick the countries to scrape, reads from dictionary dic below
countries_to_scrape = ["england"]

dic = {
        "england": {
                "code" : "E",   # used in URL
		"start_year" : 2009,
		"end_year" : 2016,
		"leagues" : [
                            ("0","prem"),  # (url_required, human_readable)
			    ("1","champ"),
			    ("2","league_1"),
			    ("3","league_2"),
		#	    ("C","conference" )
			    ],
	},
        "germany":{
                "code" : "D",
		"start_year" : 2009,
		"end_year" : 2016,
		"leagues" : [
                            ("1","bundes_1"),  
			    ("2","bundes_2"),
                            ],
        },
        "france":{
                "code" : "F",
		"start_year" : 2015,
		"end_year" : 2016,
		"leagues" : [
                            ("1","le_championnat"),  
			    ("2","div_2"),
                            ],
        },
        "italy":{
                "code" : "I",
		"start_year" : 2009,
		"end_year" : 2016,
		"leagues" : [
                            ("1","serie_a"),  
			    ("2","serie_b"),
                            ],
        },
        "spain":{
                "code" : "SP",
		"start_year" : 2009,
		"end_year" : 2016,
		"leagues" : [
                            ("1","la_liga_1"),  
			    ("2","la_liga_2"),
                            ],
        },
}

with requests.Session() as s:
    for country in countries_to_scrape: #list(dic.keys()):
        print(country)  
        country_data = dic[country]
        code = country_data["code"]
        start_year = country_data["start_year"]
        end_year = country_data["end_year"]
        leagues = country_data["leagues"]

        seasons = [str(x)[2:]+str(x+1)[2:] for x in range(start_year,end_year+1)]
        
        for season in seasons:
            for league in leagues:
                league_url = code+league[0]
                url = url_template.format(season=season,league=league_url)
                print(url)

                league_readable = league[1]
                filename = league_readable + "_" + season + ".csv"

                s.headers.update(headers)
                download = s.get(url)
                decoded_content = download.text
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                with open(data_path+filename,"w") as f:
                    writer = csv.writer(f)
                    for row in cr:
                        writer.writerow(row)
                time.sleep(np.random.uniform(low=5.0, high=15.0, size=None))
