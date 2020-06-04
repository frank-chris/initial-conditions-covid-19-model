# Initial Conditions for COVID-19 Model
Initial conditions for data-driven PDE-based modelling of Covid-19 infections

## Instructions  for Karnataka and Bengaluru

1. For Karnataka, run the Python file named computeInitialConditions.py, which will produce initial conditions for all Indian states including Karnataka. I have done this for 03 May already. 

2. For Bengaluru, run the Python file named compute_initial_districts.py(in folder Karnataka). This script is hard-coded to May 3 and only Bengaluru Urban and Bengaluru Rural, since dates for which data is available in JSON vary for each district. It can be extended if needed, but some districts will have to be left out for some dates. It can also be fully extended once I get the missing data from raw_data files.

## Instructions for states of India  

#### 1. Clone this repo  

`git clone https://github.com/frank-chris/initial-conditions-covid-19-model.git`

#### 2. Run the Python file named computeInitialConditions.py  

`python computeInitialConditions.py`

## Implementation Details  

1. The script named computeInitialConditions.py saves the initial conditions in a CSV file. 

2. The CSV file has 2 columns: 'State' and 'Initial'. 'State' has 32 state codes and Total, i.e. 33 values, and 'Initial' has the corresponding initial conditions.  

3. Currently initial conditions are written into CSV as integers. This can be changed to float by changing one line of code. 

## Data  

The state wise data used was downloaded from [here](https://api.covid19india.org/csv/).
