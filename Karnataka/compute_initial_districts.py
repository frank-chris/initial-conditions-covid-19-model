import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import lognorm
import math


def log_normal_pdf(x):
    '''
    Function to calculate PDF of a log-normal distribution
    with mu=1.62 and sigma=0.42 at a given x
    '''
    return lognorm.pdf(x, 0.42, scale = math.exp(1.62))

def daily(df):
    for column in df.columns:
        temp = df[column].sub(df[column].shift())
        temp.iloc[0] = df[column].iloc[0]
        df[column] = temp
    return df

# load the json data
f = open('districts_daily.json') 
loaded_json = json.load(f)

number_of_dates = {}

dates = []

for entry in loaded_json['districtsDaily']['Karnataka']['Bagalkote']:
    dates.append(entry['date'])


dataframes = {}

for status in ['active', 'confirmed', 'deceased', 'recovered']:
    dataframes[status] = pd.DataFrame();
    dataframes[status]['index'] = dates
    dataframes[status].set_index('index', inplace=True)
    for district in loaded_json['districtsDaily']['Karnataka'].keys():
        dataframes[status][district] = 0
        for entry in loaded_json['districtsDaily']['Karnataka'][district]:
            dataframes[status].loc[entry['date'], district] = entry[status]

active_cumulative = dataframes['active'].copy()
confirmed_cumulative = dataframes['confirmed'].copy()
deceased_cumulative = dataframes['deceased'].copy()
recovered_cumulative = dataframes['recovered'].copy()

dataframes['active'] = daily(dataframes['active'])
dataframes['confirmed'] = daily(dataframes['confirmed'])
dataframes['deceased'] = daily(dataframes['deceased'])
dataframes['recovered'] = daily(dataframes['recovered'])

initial_conditions = {}

for district in ['Bengaluru Urban', 'Bengaluru Rural']:
    initial_conditions[district] = confirmed_cumulative.loc['2020-05-03', district]
    for i, date in enumerate(dates[dates.index('2020-05-03')+1:dates.index('2020-05-03')+15]):
        initial_conditions[district] += log_normal_pdf(i+1)*dataframes['confirmed'].loc[date, district]

df = pd.DataFrame()

district = []
initial = []

for i in initial_conditions:
    district.append(i)
    initial.append(round(initial_conditions[i]))

df['district'] = district
df['initial'] = initial

df.to_csv('initial_conditions_districts.data', sep=" ", index=False)

print("\nData written to initial_conditions_districts.data\n")