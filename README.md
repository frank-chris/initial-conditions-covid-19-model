# Initial Conditions for COVID-19 Model
Initial conditions for data-driven PDE-based modelling of Covid-19 infections

## Instructions  

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
