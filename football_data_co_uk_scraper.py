"""
Scrapes CSV data from football-data.co.uk
"""

import requests
import csv
from bs4 import BeautifulSoup
import time

base_url = "http://football-data.co.uk/mmz4281/" #1617/E0.csv
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


dic = {"england": {
                "code" : "E",   # used in URL
		"start_year" : 2004,
		"end_year" : 2016,
		"leagues" : [("0","prem"),  # (url_required, human_readable)
				("1","champ"),
				("2","league_1"),
				("3","league_2"),
		#		("C","conference" )
			],
	},
        #"france":{},
}

with requests.Session() as s:
    for country in list(dic.keys()):
        print(country)  
        country_data = dic[country]
        code = country_data["code"]
        start_year = country_data["start_year"]
        end_year = country_data["end_year"]
        leagues = country_data["leagues"]

        seasons = [str(x)[2:]+str(x+1)[2:] for x in range(start_year,end_year+1)]
        
        for season in seasons:
            for league in leagues:
                league_url = league[0]
                url = base_url +  season + "/" + code+league[0] 
                print(url)

                league_readable = league[1]
                filename = league_readable + "_" + season + ".csv"
                
                s.headers.update(headers)
                download = s.get(url)
                decoded_content = download.text
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                with open(filename,"w") as f:
                    writer = csv.writer(f)
                    for row in cr:
                        writer.writerow(row)
                time.sleep(1)
