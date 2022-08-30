import sys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import counties_web_scraping  # import the counties_web_scraping.py to get the county_list
import argparse
from pathlib import Path

def get_vaccinations():
    county_list=counties_web_scraping.get_counties()[0]
    api=''
    base_url = 'https://data.cdc.gov/resource/8xkx-amqh.json'
    query='?recip_county='
    counties=[]
    date=[]
    booster=[]
    dose_1=[]
    complete=[]
    for i in county_list:
        url = base_url+query+i+api
        r = requests.get(url)
        js = r.json()
        for k in range(50):
            try:
                counties.append(i)
                d=js[k]['date']
                d=d.replace('T00:00:00.000','')
                date.append(d)
                dose=js[k]['administered_dose1_recip']
                dose_1.append(dose)
                c=js[k]['series_complete_yes']
                complete.append(c)
                b=js[k]['booster_doses']
                booster.append(b)
            except KeyError:
                dose_1.append('Na')
                complete.append('Na')
                booster.append('Na')
    return [counties,date,dose_1,complete,booster]

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
        df=pd.DataFrame(np.column_stack([get_vaccinations()[0],get_vaccinations()[1],get_vaccinations()[2],get_vaccinations()[3],get_vaccinations()[4]]),columns=['county',
                                                                                'date',
                                                                               'dose_1_numb',
                                                                               'completion_number',
                                                                              'booster_number'])
        path = 'vaccinations.csv'
        df.to_csv(path)
        print(f"Wrote data to {path}")
    with pd.option_context('display.max_rows', 5 if args.scrape else None,
                           'display.max_columns', None,
                           'display.precision', 3):
        print(df)

if __name__ == '__main__':
    main()
