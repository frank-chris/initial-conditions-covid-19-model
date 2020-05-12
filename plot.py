import pandas as pd
from scipy.stats import lognorm
import math
import matplotlib.pyplot as plt


def log_normal_pdf(x):
    '''
    Function to calculate PDF of a log-normal distribution
    with mu=1.62 and sigma=0.42 at a given x
    '''
    return lognorm.pdf(x, 0.42, scale = math.exp(1.62))

# Get date as input from user
date = input("\nEnter a date from 23-Mar-20 to 23-Apr-20\n(In the format DD-Mon-YY, eg: 24-Mar-20): ")

# State code of state to be plotted
state_code = input("\nEnter state code of the state you want to plot(eg: TN): ")

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

# List to store contributions from 14 day period
contributions = [0 for i in range(14)]

# List to store data for 14 day period that do not contribute to required date
not_contributed = [0 for i in range(14)]

# Position corresponding to initial date in date_status_list
date_index = date_status_list.index("Confirmed-"+date)+1

# Compute and fill required contributions from 14 day period 
for i, date_status in enumerate(date_status_list[date_index:date_index + 14]):
    contributions[i] += log_normal_pdf(i+1)*state_wise_daily.loc[date_status, state_code]
    not_contributed[i] += (1 - log_normal_pdf(i+1))*state_wise_daily.loc[date_status, state_code]

# 14 dates for the 14 day period
dates_14_period = [date.replace("Confirmed-", "")[:-3] for date in date_status_list[date_index:date_index + 14]]

# Plot using matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
fig.canvas.set_window_title(state_code + '-' + date) 
ax.bar(dates_14_period, not_contributed,   label= 'Not contributed to ' + date, color= "#3366CC")
ax.bar(dates_14_period, contributions,  bottom=not_contributed, label='Contributed to ' + date, color= "#DC3912")
ax.set_ylabel('Cases')
ax.set_title('Contribution of the 14 day window to ' + date + " for " + state_code)
ax.legend()

plt.show()