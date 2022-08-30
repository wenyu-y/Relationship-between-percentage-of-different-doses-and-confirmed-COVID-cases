# packaged for this final project
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import argparse
from pathlib import Path
import sys
import requests
import re

# web scrappying
def get_counties():
    url = 'https://en.wikipedia.org/wiki/List_of_counties_in_California'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    table=soup.find('table',class_='wikitable sortable')
    value=[]
    for i in table.findAll('td'):
        v=i.find('span')
        if v==None:
            continue
        else:
            value.append(v.text)
    population=[]
    area=[]
    for i in range(len(value)):
        if i%2==0:
            population.append(value[i])
        else:
            area.append(value[i])
        l=[]
    for i in table.findAll('a'):
        l.append(i.get('title'))
    li=[]
    pattern=re.compile(r'\w+\s?\w+\s?\w+\sCounty\,\s\w+')
    for j in l:
        if j==None:
            continue
        else:
            s=re.findall(pattern,j)
            if s==[]:
                continue
            else:
                li.append(s)
    new_counties=[]
    for i in li:
        for j in i:
            if j=='Lake County, Nevada':
                continue
            else:
                j=j.replace(', California','')
                new_counties.append(j)
    new_counties.insert(37,'San Francisco County')
    return new_counties,population,area
                
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
        df=pd.DataFrame(np.column_stack([get_counties()[0],get_counties()[1],get_counties()[2]]),columns=['county',
                                                                                'population',
                                                                              'area'])
        path = 'counties.csv'
        df.to_csv(path)
        print(f"Wrote data to {path}")
    with pd.option_context('display.max_rows', 5 if args.scrape else None,
                           'display.max_columns', None,
                           'display.precision', 3):
        print(df)

if __name__ == '__main__':
    main()