# packaged for this final project
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm      # fit linear regression models
import argparse
from pathlib import Path
import sys

def get_df():
    # read three datasets
    counties = pd.read_csv('data/counties.csv')
    counties=counties.drop(columns='Unnamed: 0')  #drop the index column
    community_level = pd.read_csv('data/community_level.csv')
    community_level=community_level.drop(columns='Unnamed: 0')  #drop the index column
    community_level=community_level.rename(columns={'case':'case_per_100k'})
    vaccinations=pd.read_csv('data/vaccinations.csv')
    vaccinations=vaccinations.drop(columns=['Unnamed: 0'])#drop the index column

    # concate three dataframes with their common values based on date and county
    df = pd.merge(community_level, vaccinations)
    df=pd.merge(df,counties)
    # replace Na with np.nan(NaN)
    df = df.replace(to_replace='Na', value=np.nan)
    # drop rows contains Na
    df=df.dropna()

    d=set(df['date'].values) # different three dates which closest to the date I created this project
    d=list(d)
    
    df_1=df[(df['date'] == d[0])]  # with first date within three dates list
    df_1=df_1.reset_index(drop=True)

    df_2=df[(df['date'] == d[1])]  # with second date within three dates list
    df_2=df_2.reset_index(drop=True)   

    df_3=df[(df['date'] == d[2])]  # with third date within three dates list
    df_3=df_3.reset_index(drop=True)

    df_new=df.drop(columns=['county','date','level','population','area'])
    df_new['case']=df_new['case_per_100k'].values*100000
    df_new=df_new.drop(columns=['case_per_100k'])
    df_new=df_new.reset_index(drop=True)  
    # change datatype from object to float
    df_new = df_new.astype({'dose_1_numb': np.float64,'completion_number': np.float64,'booster_number': np.float64})

    return df_1,df_2,df_3,d,df,df_new,counties,community_level,vaccinations


def get_graphs():
    # first pie graph
    sector=dict(get_df()[0]['level'].value_counts())  
    slices=list(sector.values())
    tasks=list(sector.keys())
    plt.pie(slices,labels=tasks,autopct='%1.0f%%')
    plt.legend(loc="upper right",bbox_to_anchor=(2.25,1))
    plt.title(get_df()[3][0])
    plt.show()
    # second pie chart
    sector=dict(get_df()[1]['level'].value_counts())  
    slices=list(sector.values())
    tasks=list(sector.keys())
    plt.pie(slices,labels=tasks,autopct='%1.0f%%')
    plt.legend(loc="upper right",bbox_to_anchor=(2.25,1))
    plt.title(get_df()[3][1])
    plt.show()
    # third pie chart
    sector=dict(get_df()[2]['level'].value_counts())  
    slices=list(sector.values())
    tasks=list(sector.keys())
    plt.pie(slices,labels=tasks,autopct='%1.0f%%')
    plt.legend(loc="upper right",bbox_to_anchor=(2.25,1))
    plt.title(get_df()[3][2])
    plt.show()
    # line plot
    sns.set(rc = {'figure.figsize':(15,8)})
    sns.catplot(x="county", y="case_per_100k", hue="date",kind="point", data=get_df()[4])
    #Make pairwise scatterplots of all the varianbles in the data set including the predictors with the dependent variable.
    sns.pairplot(get_df()[5])
    plt.show()

def get_analyze():
    # create multiple regression model
    #multiple regression model
    x=get_df()[5][['dose_1_numb','completion_number','booster_number']]
    y=get_df()[5]['case']
    x=sm.add_constant(x)
    model=sm.OLS(y,x).fit()
    print('multiple regression model',model.summary())
    # linear relationship between dose_1_numb and case
    x=get_df()[5][['dose_1_numb']]
    y=get_df()[5]['case']
    x=sm.add_constant(x)
    model1=sm.OLS(y,x).fit()
    print('linear relationship between dose_1_numb and case',model1.summary())
    # linear relationship between completion_number and case
    x=get_df()[5][['completion_number']]
    y=get_df()[5]['case']
    x=sm.add_constant(x)
    model2=sm.OLS(y,x).fit()
    print('linear relationship between completion_number and case',model2.summary()) 
    # linear relationship between completion_number and case
    x=get_df()[5][['booster_number']]
    y=get_df()[5]['case']
    x=sm.add_constant(x)
    model3=sm.OLS(y,x).fit()
    print('linear relationship between booster_number and case',model3.summary())

 
def main():
    parser = argparse.ArgumentParser(description='Sample scraper')
    parser.add_argument('--static',default=3,type=Path, metavar='PATH_TO_DATASET', help='Load from static path')
    args = parser.parse_args()
    if path := args.static:
        try:
            print('read first counties.csv',get_df()[6])
            print('read second community_level.csv',get_df()[7])
            print('read third vaccinations.csv',get_df()[8])
            print('concate three dataframes with their common values based on date and county',get_df()[4])
            print('we use those three dates to  create charts',get_df()[3])
            print('with first date within three dates list',get_df()[0])
            print('with second date within three dates list',get_df()[1])
            print('with third date within three dates list',get_df()[2])
            print('final dataframe to analyze and fit regression models',get_df()[5])
            print(get_graphs())
            print(get_analyze())
            print('Perform analysis on stored data')
        except:
            sys.exit(f"Could not perform analysis on stored data")
    else:
        print('read first counties.csv',get_df()[6])
        print('read second community_level.csv',get_df()[7])
        print('read third vaccinations.csv',get_df()[8])
        print('concate three dataframes with their common values based on date and county',get_df()[4])
        print('we use those three dates to  create charts',get_df()[3])
        print('with first date within three dates list',get_df()[0])
        print('with second date within three dates list',get_df()[1])
        print('with third date within three dates list',get_df()[2])
        print('final dataframe to analyze and fit regression models',get_df()[5])
        print(get_graphs())
        print(get_analyze())
        print('Perform analysis on stored data')


if __name__ == '__main__':
    main()

