import pandas as pd
from scipy.stats import lognorm
import math


def log_normal_pdf(x):
    '''
    Function to calculate PDF of a log-normal distribution
    with mu=1.62 and sigma=0.42 at a given x
    '''
    return lognorm.pdf(x, 0.42, scale = math.exp(1.62))

# Get date as input from user
date = input("\nEnter a date from 23-Mar-20 to 23-Apr-20\n(In the format DD-Mon-YY, eg: 24-Mar-20): ")

# Read csv data
state_wise_daily = pd.read_csv("state_wise_daily.csv")

# Combine the columns Status and Date to form a column named Daily_Status
state_wise_daily['Daily_Status'] = state_wise_daily["Status"] + "-" + state_wise_daily["Date"]

# Delete the columns Status and Date
del state_wise_daily['Date']
del state_wise_daily['Status']

# Delete regions that we do not need
del state_wise_daily["DN"]
del state_wise_daily["DD"]
del state_wise_daily["ML"]
del state_wise_daily["MZ"]
del state_wise_daily["NL"]

# Rename column TT as Total
state_wise_daily.rename(columns={"TT" : "Total"}, inplace=True)

# Move the column Total to the end
column_total = state_wise_daily.pop("Total") 
state_wise_daily["Total"] = column_total

# A list of elements from Daily_Status
date_status_list = state_wise_daily["Daily_Status"]

# Filter out recovered and deceased cases from the list
date_status_list = [date_status for date_status in date_status_list if "Confirmed" in date_status]

# Set the column Daily_Status as the index of the DataFrame 
state_wise_daily.set_index("Daily_Status", inplace = True) 

# List of column names
columns_list = state_wise_daily.columns

# List for storing data to be written into a file
initial_conditions_list = [0 for x in range(33)]

# Position corresponding to initial date in date_status_list
date_index = date_status_list.index("Confirmed-"+date)+1

# Compute and fill required initial conditions data into dict 
for k, column in enumerate(columns_list):
    initial_conditions_list[k] = 0
    for date_status in date_status_list[:date_index]:
        initial_conditions_list[k] += state_wise_daily.loc[date_status, column]
    for i, date_status in enumerate(date_status_list[date_index:date_index + 14]):
        initial_conditions_list[k] += log_normal_pdf(i+1)*state_wise_daily.loc[date_status, column]
    initial_conditions_list[k] = round(initial_conditions_list[k])

# Pandas DataFrame to store initial conditions
initial_conditions_df = pd.DataFrame()

initial_conditions_df["State"] = columns_list
initial_conditions_df["Initial"] = initial_conditions_list

# Write initial conditions DataFrame to csv file
initial_conditions_df.to_csv(date + '-initial.csv', index=False)

print("\nData written into " + date + '-initial.csv\n')

