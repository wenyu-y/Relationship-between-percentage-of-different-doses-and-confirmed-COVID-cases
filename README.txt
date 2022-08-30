# NOTE
I have add an updated code for HW4 file to makeup half of losing points in HW4. Thank you.

# How to run my code
There are two parts to run codes for this project:

1. First, you need to run the codes from updated code for HW4 subfolder to obtain 3 datasets. Those 3 datasets are also stored in the data subfolder just in case. In the updated code for HW4, there are 3 .py files community_level_api.py, counties_web_scraping.py, and vaccinations_api.py. Run each .py file in the terminal and the datasets will be stored as a .csv file.

	There are three example commands you can use in the terminal:
	1. python3 community_level_api.py --static /Users/yangwenyu/Desktop/finalproject/data/community_level.csv  #you can use any three of the .py in updated code for HW4 folder and corresponding .csv file.

	3. python3 community_level_api.py --scrape  #return only 5 entires
# you also can use any of the .py in updated code for HW4 folder

	2. python3 community_level_api.py  OR  python3 counties_web_scraping.py OR python3 vaccinations_api.py



2. Second, you need to run the FinalProject_Wenyu_Yang.py in the terminal. All the data frames, graphs, and results of regression models will be shown. 

    There are two example commands you can use in the terminal:
	1. python3 FinalProject_Wenyu_Yang.py --static /Users/yangwenyu/Desktop/finalproject/data/vaccinations.csv  #you can use any three of the .csv in data folder to perform and obtain results of FinalProject_Wenyu_Yang.py 

	2. python3 FinalProject_Wenyu_Yang.py 


# packages required for this project
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm      # fit linear regression models
import warnings
warnings.filterwarnings("ignore")
import sys
import requests
import json
import counties_web_scraping  # import the counties_web_scraping.py to get the county_list
import argparse
from pathlib import Path
