# -*- coding: utf-8 -*-
"""
Created on Mon Jun  10 22:22:17 2020
@author: JONATHAN CHAN and SIRISHA PANDRAMISHI

#checkpoint: address PR feedback: https://github.ubc.ca/ltian05/better_dwelling_capstone/pull/6#issuecomment-16602
"""
import pandas as pd
from datetime import datetime
import datetime as dt
import os
import calendar
from calendar import monthrange

#define where manually downloaded indicator data files reside
filename = "../data/financial_indicator_data/"

def update_datetime_end(dt_object):
    """returns a datetime object with the day field updated to the last day of the month(leap years included)"""
    new_year = dt_object.year
    new_month = dt_object.month
    new_day = calendar.monthrange(new_year, new_month)[1]
    
    new_dt = dt.datetime(year=new_year, month=new_month, day=new_day)
    return new_dt

def get_gdp_df(path):
    """
    Preprocess the csv file containing the manually downloaded GDP data 
    
    Data source: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610010401
    
    Returns a dataframe with date, indicator, and value columns:
    date: YYYY-MM-DD 
    indicator: GDP
    value: year-over-year percent change of monthly GDP
    
    input:
    path: filepath to input csv file containing GDP data
    start_date: string in YYYY-MM-DD format
    end_date:  string in YYYY-MM-DD format
    
    Assume start_date and end_date are contained within the input csv file

    
    """
    try:
        df = pd.read_csv(path)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None

    #get data from most recent to the past year
    start_date = datetime.strptime("2019-04-01", "%Y-%m-%d")
    end_date = datetime.strptime("2020-04-01", "%Y-%m-%d")


    ## select only all industries
    df = df.loc[df['North American Industry Classification System (NAICS)'].values == 'All industries [T001]']
    # Add dummy day as first day of the month
    df['REF_DATE'] = (df['REF_DATE'] + "-01")
    # Convert the column to datetime type from string type
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    #Update datetime day to the end of month for viz
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: update_datetime_end(x))
    #Scale adjusted to millions (so multiply by 1 million)
    df['VALUE'] = df['VALUE']*1000000
    # Create new dataframe with only required columns : date and gdp value
    gdp_df =  pd.concat([df['REF_DATE'], df['VALUE']], axis=1, keys=['date', 'value'])
    # Create a new column for indicator
    gdp_df.insert(loc=1, column='indicator', value="GDP")


    # create a new_column and sort by date
    gdp_df['percentage_change'] = 0.0
    gdp_df = gdp_df.sort_values('date')

    for i in range(0,gdp_df.shape[0]):
        date_column = gdp_df['date'][i]
        #print(date_column)
        if start_date <= date_column <= end_date:
            date_offset = date_column - pd.offsets.DateOffset(years=1)
    #    one year ago date column  is  date_offset)
            filtered_df = gdp_df[(gdp_df.date == date_offset)]
            #print(filtered_df)
            gdp_df['percentage_change'][i] = ( (gdp_df['value'][i]-filtered_df['value'])/filtered_df['value'])*100

    # Drop the data for less than 1 year
    for i in range(gdp_df.shape[0]):
        # Dates where we want to consider the data
        date_column = gdp_df['date'][i]    
        if start_date <= date_column <= end_date:
            pass
        else:
            gdp_df = gdp_df.drop(gdp_df[(gdp_df.date == date_column)].index)

    gdp_df = gdp_df.drop(columns=["value"])
    gdp_df = gdp_df.rename(columns={"percentage_change": "value"})
    
    #tests
    assert(gdp_df["date"].dtype == "datetime64[ns]")
    assert(gdp_df["indicator"].dtype == "object")
    assert(gdp_df["value"].dtype == "float64")
    #check that value column is a percentage
    assert (gdp_df['value'] < 100).all() & (gdp_df['value'] > -100).all()
    
    return gdp_df

def get_tsx_df(path):
    """
    
    Preprocess the csv file containing the manually downloaded TSX data 
    
    Data source: https://ca.finance.yahoo.com/quote/%5EGSPTSE/history?period1=1546300800&period2=1592438400&interval=1mo&filter=history&frequency=1mo
    
    Returns a dataframe with date, indicator, and value columns:
    date: YYYY-MM-DD 
    indicator: TSX
    value: TSX close value of that date
    
    input:
    path: filepath to input csv file containing TSX data

    Assume input csv starts and ends with the desired values
    Assume input csv has a 'Close' column
    """
    try:
        df = pd.read_csv(path)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None
    
    # Convert the column to datetime type from string type
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    #Update datetime day to the end of month for viz
    df['Date'] = df['Date'].apply(lambda x: update_datetime_end(x))
    # Create new dataframe with only required columns : date and Close values
    tsx_df = pd.concat([df['Date'], df['Close']], axis=1, keys=['date', 'value'])
    # Create a new column for indicator
    tsx_df.insert(loc=1, column='indicator', value="TSX")
    
    #tests
    assert(tsx_df["date"].dtype == "datetime64[ns]")
    assert(tsx_df["indicator"].dtype == "object")
    assert(tsx_df["value"].dtype == "float64")
    
    return tsx_df

def get_mortgage_df(path):
    """
    Preprocess the csv file containing the manually downloaded mortgage rate data 
    
    Data source: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1010000601 
    
    Returns a dataframe with date, indicator, and value columns:
    date: YYYY-MM-DD 
    indicator: TSX
    value: Total, funds advanced, residential mortgages, insured
    
    input:
    path: filepath to input csv file containing mortgage rate data

    Assume relevant information is contained within input csv rows where:
        "Unit of measure" column has value "Interest rate"
        "Components" column has value "Total, funds advanced, residential mortgages, insured"
    """
    
    try:
        df = pd.read_csv(path)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None
    
    df = pd.read_csv(path)
    ## select only "Interest rates" and "Total, funds advanced, residential mortgages, insured"
    df = df[(df['Unit of measure'] == "Interest rate" )& (df['Components'] == "Total, funds advanced, residential mortgages, insured")]
    # Add dummy day as first day of the month
    df['REF_DATE'] = (df['REF_DATE'] + "-01")
    # Convert the column to datetime type from string type
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    #Update datetime day to the end of month for viz
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: update_datetime_end(x))
    # Create new dataframe with only required columns : date and gdp value
    mortgage_rate_df =  pd.concat([df['REF_DATE'], df['VALUE']], axis=1, keys=['date', 'value'])
    # Create a new column for indicator
    mortgage_rate_df.insert(loc=1, column='indicator', value="mortgage_rate")
    
    #tests
    assert(mortgage_rate_df["date"].dtype == "datetime64[ns]")
    assert(mortgage_rate_df["indicator"].dtype == "object")
    assert(mortgage_rate_df["value"].dtype == "float64")
    
    return mortgage_rate_df

def get_interest_df(path):
    """
    
    Preprocess the csv file containing the manually downloaded interest rate data 
    
    Data source: https://www.bankofcanada.ca/rates/interest-rates/canadian-interest-rates/?rangeType=dates&rangeValue=1&rangeWeeklyValue=1&rangeMonthlyValue=1&ByDate_frequency=daily&lP=lookup_canadian_interest.php&sR=2010-06-02&se=L_V39079&dF=2019-06-02&dT=2020-06-02
    
    Returns a dataframe with date, indicator, and value columns:
    Date: YYYY-MM-DD 
    indicator: interest_rate
    value: value of overnight target interest rate
    
    input:
    path: filepath to input csv file containing interest rate data

    Assume all rows in input csv are relevant
    Assume header is 11 lines
    """
    
    try:
        boc_interest_rates_df = pd.read_csv(path, skiprows=11)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None

    boc_interest_rates_df.insert(loc=1, column='indicator', value="interest_rate")
    boc_interest_rates_df["Date"] = pd.to_datetime(boc_interest_rates_df["Date"], format="%Y-%m-%d")
    boc_interest_rates_df = boc_interest_rates_df.sort_values(by='Date')
    boc_interest_rates_df =boc_interest_rates_df.rename(columns={"V39079": "value"})
    
    #tests
    assert(boc_interest_rates_df["Date"].dtype == "datetime64[ns]")
    assert(boc_interest_rates_df["indicator"].dtype == "object")
    assert(boc_interest_rates_df["value"].dtype == "float64")
    return boc_interest_rates_df

def get_employment_df(path):
    """
    Preprocess the csv file containing the manually downloaded employment data 
    
    Data source: https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1410001701 
    
    Returns a dataframe with date, indicator, and value columns:
    date: YYYY-MM-DD 
    indicator: interest_rate
    value: employment rates
    
    input:
    path: filepath to input csv file containing employment data

    Assume relevant information is contained within input csv rows where:
        "Sex" column has value "Both sexes"
        "Age group" has value "15 years and over"
        "GEO" column has value "Canada"
    """
    try:
        df = pd.read_csv(path)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None
    
    df = df[(df["Sex"] == "Both sexes" )& (df['Age group'] == "15 years and over") & (df['GEO'] == "Canada")]

    ## select only "Both sexes" 
    # df = df.loc[df['Sex'].values == "Both sexes" ]
    # Add dummy day as first day of the month
    df['REF_DATE'] = (df['REF_DATE'] + "-01")
    # Convert the column to datetime type from string type
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    #Update datetime day to the end of month for viz
    df['REF_DATE'] = df['REF_DATE'].apply(lambda x: update_datetime_end(x))
    # Create new dataframe with only required columns : date and gdp value
    employment_df =  pd.concat([df['REF_DATE'], df['VALUE']], axis=1, keys=['date', 'value'])
    # Create a new column for indicator
    employment_df.insert(loc=1, column='indicator', value="employment")
    
    #tests
    assert(employment_df["date"].dtype == "datetime64[ns]")
    assert(employment_df["indicator"].dtype == "object")
    assert(employment_df["value"].dtype == "float64")
    
    return employment_df

def get_housing_df(path):
    """
    Preprocess the csv file containing the manually downloaded housing price data 
    
    Data source: https://www.crea.ca/housing-market-stats/mls-home-price-index/hpi-tool/
    
    Returns a dataframe with date, indicator, and value columns:
    date: YYYY-MM-DD 
    indicator: interest_rate
    value: percentage growth in the composite HPI value
    
    input:
    path: filepath to input csv file containing housing price data

    Assume relevant information is contained within rows that either:
        "year" column has value '2019', or 
        "year" column has value '2020'
    """
    
    try:
        df = pd.read_csv(path)
    except:
        print("PATH DOES NOT EXIST: ", path)
        return None

    df['Date'] = pd.to_datetime(df['Date'], format='%b %Y')
    housing_price_df =  pd.concat([df['Date'], df['Composite_HPI']], axis=1, keys=['date', 'value'])
    housing_price_df.insert(loc=1, column='indicator', value="housing_price")
    housing_price_df['year'] = housing_price_df['date'].apply(lambda x: x.year)

    housing_price_df = housing_price_df[(housing_price_df["year"] == 2019 ) | (housing_price_df["year"] == 2020 ) ]

    housing_price_df =housing_price_df.drop(columns = ['year'])

    housing_price_df.reset_index(drop=True, inplace=True)

    housing_price_df['percentage_change'] = 0.0

    for i in range(1,housing_price_df.shape[0]):
        housing_price_df['percentage_change'][i] = ((housing_price_df['value'][i] - housing_price_df['value'][i-1])/housing_price_df['value'][i])*100

    housing_price_df = housing_price_df.drop(columns=["value"])
    housing_price_df = housing_price_df.rename(columns={"percentage_change": "value"})
    #Update datetime day to the end of month for viz
    housing_price_df['date'] = housing_price_df['date'].apply(lambda x: update_datetime_end(x))
    
    #tests
    assert(housing_price_df["date"].dtype == "datetime64[ns]")
    assert(housing_price_df["indicator"].dtype == "object")
    assert(housing_price_df["value"].dtype == "float64")
    #check that value column is a percentage
    assert (housing_price_df['value'] < 100).all() & (housing_price_df['value'] > -100).all()
    
    return housing_price_df

def df_to_merge(df, indicator_name):
    """returns a two column dataframe from a three column dataframe
    
    order of columns -input: date, type of indicator, value of indicator
    order of columns - output: date, value of indicator w/ indicator in column name
    
    """

    df_to_merge = df
    val_name = "value_" + indicator_name
    df_to_merge.columns = ['date', 'ind', val_name]
    df_to_merge = df_to_merge.drop(columns=["ind"])
    
    return df_to_merge


def main():
    
    #create six individual dataframes
    try:
        gdp_path = filename + "gdp.csv"
        gdp_start = "2019-04-01"
        gdp_end = "2020-03-01"
        gdp_df = get_gdp_df(gdp_path)

        tsx_path = filename + 'tsx.csv'
        tsx_df = get_tsx_df(tsx_path)

        mortgage_rate_path = filename + 'mortgagerates.csv'
        mortgage_rate_df = get_mortgage_df(mortgage_rate_path)

        employment_path = filename + 'employment.csv'
        employment_df = get_employment_df(employment_path)

        interest_rates_path = filename + 'interestrates.csv'
        boc_interest_rates_df = get_interest_df(interest_rates_path)

        housing_path = filename + 'housing.csv'
        housing_price_df = get_housing_df(housing_path)
    except:
        print("Error in get_INDICATOR_df() functions - check file structure in " + filename)
        return None
    
    #create dataframes with value_indicator column name
    try:
        gdp_to_merge = df_to_merge(gdp_df, "GDP")
        tsx_to_merge = df_to_merge(tsx_df, "TSX")
        mort_to_merge = df_to_merge(mortgage_rate_df, "mortgage_rates")
        employment_to_merge = df_to_merge(employment_df, "employment")
        housing_to_merge = df_to_merge(housing_price_df, "housing_prices")
        intr_to_merge = df_to_merge(boc_interest_rates_df, "interest_rates")  
    except:
        print("Error in df_to_merge() function - check dataframe inputs")
        return None
    
    
    #merge dataframe into full dataframe
    total_df = None
    total_df = gdp_to_merge.merge(tsx_to_merge, how="outer")
    total_df = total_df.merge(mort_to_merge, how="outer")
    total_df = total_df.merge(employment_to_merge, how="outer")
    total_df = total_df.merge(housing_to_merge, how="outer")
    total_df = total_df.merge(intr_to_merge, how="outer")
    total_df = total_df.sort_values(by='date')
    
    assert total_df.shape[1] == 7, "incorrect number of columns (1 date column + 6 indicator columns)"
    
    #export_to_csv
    out_filename= "combined_indicator_data.csv"
    
    if not os.path.exists(out_filename):
        try:
            total_df.to_csv(out_filename, index = False)
            print("FINANCIAL INDICATOR FILE CREATED: ", out_filename)
            print("ROWS, COLUMNS IN FILE: ", total_df.shape)
        except:
            print("Error in outputting csv - check total_df format")
    else:
        print("FINANCIAL INDICATOR FILE ALREADY EXISTS: ", out_filename)
    

if __name__ ==  '__main__':
    main()

