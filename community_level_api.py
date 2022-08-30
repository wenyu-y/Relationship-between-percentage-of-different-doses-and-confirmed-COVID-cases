# packaged for this final project
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path
import sys
import requests
import counties_web_scraping  # import the counties_web_scraping.py to get the county_list

# External API
def get_community_level():
    county=counties_web_scraping.get_counties()[0]
    api=''
    base_url = 'https://data.cdc.gov/resource/3nnm-4jni.json'
    query='?county='
    query2='&state=California'
    counties=[]
    date=[]
    level=[]
    cases=[]
    for i in county:
        url = base_url+query+i+query2+api
        r = requests.get(url)
        js = r.json()
        for k in range(7):
            counties.append(pd.Series(i))
            d=js[k]['date_updated']
            d=d.replace('T00:00:00.000','')
            date.append(d)
            l=js[k]['covid_19_community_level']
            level.append(l)
            c=js[k]['covid_hospital_admissions_per_100k']
            cases.append(c)
    return [counties,date,level,cases]

def main():
    parser = argparse.ArgumentParser(description='Sample scraper')
    parser.add_argument('--scrape', action=argparse.BooleanOptionalAction, default=False, help='Show only 5 entries')
    parser.add_argument('--static', type=Path, metavar='PATH_TO_DATASET', help='Load from static path')
    args = parser.parse_args()
    if path := args.static:
        try:
            df = pd.read_csv(path)
            print(f"Read data from {path}")
        except:
            sys.exit(f"Could not read {path}")
    else:
        df=pd.DataFrame(np.column_stack([get_community_level()[0],get_community_level()[1],get_community_level()[2],get_community_level()[3]]),columns=['county','date','level','case'])
        path = 'community_level.csv'
        df.to_csv(path)
        print(f"Wrote data to {path}")
    with pd.option_context('display.max_rows', 5 if args.scrape else None,
                           'display.max_columns', None,
                           'display.precision', 3):
        print(df)

if __name__ == '__main__':
    main()
