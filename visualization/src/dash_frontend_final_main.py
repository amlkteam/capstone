# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:35:10 2020

# a whole script combining reading in data of indicators_df, combined_senti_df,\
 plot charts in Plotly and rendering the frontend interface with Dash
@author: Amy, Jon, Aaron

#checkpoint Jun6 1:44pm-- graph can now narrow down corresponding to date-picker-ranger
#checkpoint Jun8 1pm Jon modified tooltip, label colors, axis limits
#checkpoint Jun8 2pm extended hoverlabel namelength

"""
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import datetime
from datetime import datetime as dt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import random
from scipy.stats import pearsonr
import re
import urllib


def generate_raw_sentiment_score(row):
    '''calculate sentiment score based on best_label'''
    if row['best_label'] == 1:
        result = row['best_confidence'] + 0.5
    elif row['best_label'] == -1:
        result = -row['best_confidence'] - 0.5
    else:
        # total = row['best_confidence'] + row['second_confidence'] + row['least_confidence'] these add up to 1
        if row['second_likely'] == 1:
            result = row['second_confidence'] - row['least_confidence']
        else:
            result = row['least_confidence'] - row['second_confidence']
    return result

def get_raw_sentiment_score(csvpath):
    '''outputs a dataframe that contains the raw sentiment score for all the articles'''
    df = pd.read_csv(csvpath)
    df['publishedAt'] = df['publishedAt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    df['raw_sentiment_score'] = df.apply(lambda row: generate_raw_sentiment_score(row), axis=1)
    return df

def get_monthly_avg_score(df):
    """
    Calculate the monthly average sentiment scores for one indicator of one source.
    
    input:
    df: a dataframe that includes the raw sentiment scores of prediction
    
    output:
    A one column dataframe, the index of which is date (publishedAt) which represents 
    the month of the average score. The monthly_avg_sent_score column is the 
    average sentiment score.
    
    """
    
    ave_df = df.resample('M').mean()
    ave_df = ave_df[['raw_sentiment_score']].rename(columns={'raw_sentiment_score': 'monthly_avg_sent_score'})
    ## the reason we use 'ffill' here is that if there is no articles in the next month, then we assume that the sentiment of the market doesn't change

    ave_df = ave_df.fillna(method='ffill')
    return ave_df

def plot_combined_graph_new(indicator_df, senti_df, indicator_name="y-axis label", title="Default Title", add_rangeslide=True): 
    """
    returns a Plotly graph given a dataframes containing financial indicator data and 
    a dataframe containing sentiment values, to visualize monthly-average sentiment change against the selected indicator.
 
    INPUT:
    indicator_df: dataframe containing a "date" column of datetimes and a "values" column of float values
    senti_df: dataframe containing a "final_sentiment" column of float values
    indicator_name: string label for y axis (what is tracked in indicator_df["values"])
    title: string of title 
    add_rangeslide: boolean of displaying
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    ## indicators_df has one independent y-axis and senti_df has another y-axis as they're not different scale 
    ## date ranges of indicator_df also differs from that of senti_df

    indi_y = indicator_df["values"].astype('float64')
    indi_dates = indicator_df["dates"].astype('datetime64[ns]')
    
    senti_y = senti_df["final_sentiment"].astype('float64')
    senti_dates = senti_df.index.astype('datetime64[ns]') 
    
    
    #set x axis limits for visualization
    x_axis_limit_l = max([min(indi_dates), min(senti_dates)]) #latest of two start periods
    x_axis_limit_r = min([max(indi_dates), max(senti_dates)]) #earliest of two end periods
    #Add indicator area visualization - set boundaries, add to fig object, update axis
    indi_axis_min = min(indi_y) - 0.1
    indi_axis_max = max(indi_y) + 0.1
    fig.add_trace(
        go.Scatter(x=indi_dates, 
                   y=indi_y, 
                    name=indicator_name,
                    fill='tonexty', 
                    mode='lines', 
                    line_color='#1d8716',
                    hoverlabel={'namelength':-1},
                    hovertemplate =
                    '<b>Value: </b>: %{y:.4f}'+
                    '<br><b>Date:</b>: %{x}<br>'),
                    secondary_y=False)
    fig['layout']['yaxis1'].update(title=indicator_name, 
                                   range=[indi_axis_min, indi_axis_max], 
                                   autorange=False)
    #Add sentiment line visualization - set boundaries, add to fig object, update axis
    senti_axis_min = -2.5 #slightly smaller than min neg sentiment value of -2
    senti_axis_max = 2.5 #slightly larger than max pos sentiment value of 2

    fig.add_trace(
        go.Scatter(x=senti_dates, 
                   y=senti_y,
                    hovertemplate =
                    '<b>Monthly average sentiment: </b>: %{y:.4f}'+
                    '<br><b>Date:</b>: %{x}<br>',

                   name="sentiment score", ## we should change this? 
                  line_color='#011269',
                  hoverlabel={'namelength':-1}),
                    secondary_y=True)
    
    fig['layout']['yaxis2'].update(title='Sentiment Score', 
                                   range=[senti_axis_min, senti_axis_max],
                                  tickvals=[-2, 0, 2],
                                  ticktext=["negative", "neutral", "positive"],
                                   color="#011269"
                                  )
    #update x axis, add title, and show
    fig.update_xaxes(rangeslider_visible=add_rangeslide,
                     range = [x_axis_limit_l, x_axis_limit_r],
                     title_text="Date",)
    
    fig.update_layout(title_text=title,
                     legend=dict(x=0.0, y=-0.7))
    
    return fig

def plot_combined_graph_scatter(indicator_df, senti_df, indicator_name="y-axis label", title="Default Title", add_rangeslide=True): 
    """
    returns a Plotly graph given a dataframes containing financial indicator data and 
    a dataframe containing sentiment values, to visualize daily sentiment change against the selected indicator.
 
    INPUT:
    indicator_df: dataframe containing a "date" column of datetimes and a "values" column of float values
    senti_df: dataframe containing a "final_sentiment" column of float values
    indicator_name: string label for y axis (what is tracked in indicator_df["values"])
    title: string of title 
    add_rangeslide: boolean of displaying
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    indi_y = indicator_df["values"].astype('float64')
    indi_dates = indicator_df["dates"].astype('datetime64[ns]') 
    senti_y = senti_df["final_sentiment"].astype('float64')
    
    senti_dates = senti_df.index.astype('datetime64[ns]')

    if "title_desc" in senti_df.columns:
        print('senti_df["title_desc"] exists')
        senti_titledesc = [x[:80]+str("...") for x in senti_df["title_desc"]] #limit to 80 characters per title
    else:
        senti_titledesc = []
    
    
    #set x axis limits for visualization
    x_axis_limit_l = max([min(indi_dates), min(senti_dates)]) #latest of two start periods
    x_axis_limit_r = min([max(indi_dates), max(senti_dates)]) #earliest of two end periods
    #Add indicator area visualization - set boundaries, add to fig object, update axis
    indi_axis_min = min(indi_y) - 0.1
    indi_axis_max = max(indi_y) + 0.1
    fig.add_trace(
        go.Scatter(x=indi_dates, 
                   y=indi_y, 
                    name=indicator_name,
                    #fill="tozeroy",
                    mode='lines', 
                    line_color='#0bab00',
                    hoverlabel={'namelength':-1},
                    hovertemplate =
                    '<b>Value: </b>: %{y:.4f}'+
                    '<br><b>Date:</b>: %{x}<br>'),
                    secondary_y=False)
    fig['layout']['yaxis1'].update(title=indicator_name, 
                                   range=[indi_axis_min, indi_axis_max],
                                   autorange=False)
    #Add sentiment line visualization - set boundaries, add to fig object, update axis
    senti_axis_min = min(senti_y) - 1
    senti_axis_max = max(senti_y) + 1
    fig.add_trace(
        go.Scatter(
            x=senti_dates, 
            y=senti_y,
            
            #text=senti_df["title_desc"],
            #hovertemplate =
            #'<b>Article Sentiment: </b>: %{y:.3f}'+
            #'<br><b>Date:</b>: %{x}<br>',
            mode="markers",
            opacity=0.75, #0.95
            name="Sentiment Score",
            hoverlabel={'namelength':-1},
            hovertext=senti_titledesc, 
            
            #hoverinfo='x+y+text',
            
            #texttemplate='%{text:15}',
            marker=dict(
                color="#011269"
            )
        ),
        secondary_y=True
    )
    fig['layout']['yaxis2'].update(title='Sentiment Score', 
                                   range=[senti_axis_min, senti_axis_max],
                                tickvals=[-2, 0, 2],
                                  ticktext=["negative", "neutral", "positive"],
                                color="#690154")
    #update x axis, add title, and show
    fig.update_xaxes(rangeslider_visible=add_rangeslide,
                     range = [x_axis_limit_l, x_axis_limit_r],
                     title_text="Date")
    fig.update_layout(title_text=title,
                     legend=dict(x=0.0, y=-0.7))
    
    return fig

# weighted-average sentiment calculation function from Aaron

def monthly_weighted_average(source_dict):
    """
    Calculate the monthly weighted average sentiment score for indicators such as 
    GDP, employment rate, housing index, stock index, and mortgage rate.
    output is a one columns dataframe, the index of which is the date (publishedAt) 
    of the weighted average sentiment score, the weighted_ave_sent_score column is 
    the weighted average sentiment scores calculated from multiple sources. 
    
    inputs:
    source_dict: a dictionary of different sources. The key of the dictionary are the 
                 names of news sources. The value of the dictionary are lists, the first 
                 element of the list is the dataframe of the news source that includes 
                 the predicted monthly average sentiment score, the second element is the
                 weight of that news source.
    """
    df_list = []
    for value_pair in source_dict.values():
        df = value_pair[0]
        df = df['monthly_avg_sent_score'] * value_pair[1]
        df = df.to_frame()
        df_list.append(df)
        
        if len(df_list) > 1:
            df_list[0] = df_list[0].add(df_list[1], fill_value=0)
            
    out_df = df_list[0].rename(columns={'monthly_avg_sent_score': 'monthly_weighted_ave_sent_score'})
    return out_df

def daily_weighted_average(daily_senti_df, source_weight_dict): 
    
    '''
    Calculates daily weighted average sentiment scores for days that have more than 1 source, 
    given a dataframe containing predictions with daily frequency and a dictionary containing weight for each source.    
    '''
    
    same_dates_index =daily_senti_df[daily_senti_df.groupby(level=0).size() > 2].index #> 50 days

    daily_senti_df['source_wgt'] = daily_senti_df['source'].apply(lambda x: source_weight_dict[x])
    daily_senti_df['weighted'] = daily_senti_df['raw_sentiment_score']  * daily_senti_df['source_wgt']

    wgted_dates = daily_senti_df.loc[same_dates_index].resample('D',level=0).mean().dropna()
    wgted_daily_scores = wgted_dates.weighted
    raw_daily_scores = daily_senti_df.loc[~daily_senti_df.index.isin(same_dates_index)].raw_sentiment_score
    weighted_series = pd.concat([wgted_daily_scores,raw_daily_scores]).sort_index()
    daily_avg_df = weighted_series.to_frame()
    daily_avg_df.columns=['final_sentiment']

    return daily_avg_df.drop_duplicates(keep='first') 

def get_correlation(aggregate_df, indicator_df, indicator, source, start_date=None, end_date=None):
    """
    calculate the Pearson’s correlation between monthly sentiment score
    of an indicator from a source and the values of that economic indicator.
    
    inputs:
    aggregate_df:   The aggregated sentiment dataframe that includes both annotated and 
                    predicted data for under each indicator and each source.
                    
    indicator_df:   The dataframe that contains all the indicators values.
    
    indicator:      The indicator that the user has chosen
    source:         The source that the user picked
    start_date:     The start date the user picked
    end_date:       The end date the user has picked
    """
    
    indi_colname_dict = {'GDP':'value_GDP', 'employment':'value_employment', 'housing prices': 'value_housing_prices', 'interest rates': 'value_interest_rates', 'mortgage rates': 'value_mortgage_rates', 'TSX': 'value_TSX'}
    senti_colname_dict = {'GDP':'gdp', 'employment':'employment', 'housing prices':'housing','interest rates': 'interest', 'mortgage rates':'mortgage','TSX': 'stock'}
    
    economic_indicator = indi_colname_dict[indicator]
    senti_indicator = senti_colname_dict[indicator]
    

    if source == 'Source-weighted Average':
        #pass # Need to add something here to call the monthly weighted avg
        senti_df = aggregate_df.query('indicator == @senti_indicator')
        source_dict = {}
        for src in list(source_wgt_dict.keys()):
            source_df_subset = get_monthly_avg_score(senti_df.query(' source == @src '))
            source_dict[src] = [source_df_subset, source_wgt_dict[src]]
            
        senti_monthly_avg = monthly_weighted_average(source_dict).dropna()
        
    else:
        if source == 'All sources':
            senti_df = aggregate_df.query('indicator == @senti_indicator')
        else:
            senti_df = aggregate_df.query('indicator == @senti_indicator & source == @source ')
    
        senti_monthly_avg = get_monthly_avg_score(senti_df).dropna()
    
    indi_monthly_avg = indicator_df[economic_indicator].to_frame().resample('M').mean().dropna()
    
    earliest = max(min(indi_monthly_avg.index), min(senti_monthly_avg.index))
    latest = min(max(indi_monthly_avg.index), max(senti_monthly_avg.index))
    
    if not start_date or start_date < earliest:
        start_date = earliest
        
    if not end_date or end_date > latest:
        end_date = latest
        
    senti_subset = senti_monthly_avg[start_date:end_date]
    indi_subset = indi_monthly_avg[start_date:end_date]
    assert(len(senti_subset) == len(indi_subset))
    
    if len(senti_subset) == 0:
        print('please select valid dates!')
        return
    
    senti_subset_list = senti_subset.iloc[:,0].to_list()
    indi_subset_list = indi_subset.iloc[:,0].to_list()
    
    corr, _ = pearsonr(senti_subset_list, indi_subset_list)
    
    return corr

# dictionary of y-axis labels from Jon

indic_to_value = {}
indic_to_value["value_GDP"] = "GDP <br>(year-on-year percentage growth)"
indic_to_value["value_TSX"] = "S&P/TSX Composite Index <br>(close value)"
indic_to_value["value_mortgage_rates"]= "Mortgage Rate <br>(residential, insured)"
indic_to_value["value_housing_prices"] = "Home Price Index  <br> (month-on-month percentage growth)"
indic_to_value["value_employment"] = "Employment Rate <br>(All genders, 15+ years old)"
indic_to_value["value_interest_rates"] = "Interest Rate <br>(overnight target rate)"

#giant indicators df imported
indicators_df_path = r'../data/combined_indicator_data.csv'
senti_df_path = r"../data/combined_sentiment_data.csv"

def main(indicators_df_path, senti_df_path):

    indicators_df = pd.read_csv(indicators_df_path, parse_dates=['date'])
    #read in sentiment data
    combined_senti_df = pd.read_csv(senti_df_path,parse_dates=    ['publishedAt'],index_col='publishedAt')


    ## main function of Dash app frontend

    indicators = ['GDP','mortgage rates','interest rates','employment','housing prices','TSX']
    sources = ['All sources','Source-weighted Average','Bloomberg','CBC']
    default_indicator = 'GDP'
    default_source = 'All sources'

    senti_colname_dict = {'GDP':'gdp', 'employment':'employment', 'housing prices':'housing','interest rates': 'interest', 'mortgage rates':'mortgage','TSX': 'stock'}
    source_wgt_dict = {'Bloomberg': 0.7, 'CBC': 0.3}

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        
        
        html.H3("Canadian News Sentiment Swings As Economy Evolves"),
        
        html.Div([
            
        html.Div([
                
        html.P("Pick an economic indicator and a news source: "),
        
        dcc.Dropdown(
                    id='indicator-name',
                    options=[{'label': i[0].capitalize()+i[1:], 'value': i} for i in indicators],
                    value=default_indicator, # set a default value
                    optionHeight = 30
                ),
        
        dcc.Dropdown(
                    id='source-name',
                    options=[{'label': i, 'value': i} for i in sources],
                    value=default_source, # set a default value
                    optionHeight = 30
                ),
        
        html.Br(),
            
        html.Div([
        html.Label("Pick a chart type: ",style={'display':'inline-block'}),
        dcc.RadioItems(
            id = 'chart-type',
            options=[
                {'label': 'Monthly average', 'value': 'line'},
                {'label': 'Daily datapoints', 'value': 'scatter'}
            ],
            value='line',
            labelStyle={'display': 'inline-block'}
        )])
            ]),
        
        html.Div([
        html.Em(id='correlation-coef'),
        html.Label(' in the period'),
            
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=dt(2010, 1, 1),
            #max_date_allowed=dt(2017, 9, 19),
            initial_visible_month=dt(2020, 6, 1),
            start_date=dt(2019, 1, 1).date(), #set default start_date to the earliest date of available data
            end_date=dt(2020, 6, 1).date() #set default end_date to the latest date of available data
        ),

        ]),
        
        
        ]), #style={'columnCount': 2}
        

        
        dcc.Graph(id = 'indicator-senti-graph'), #figure=test_fig
        
        html.P("Notes: "),
        
        html.P(" * Daily datapoints of news article sentiment is a combination of customized sentiment analyzer model predictions plus hand-made golden annotations."),
        
        html.P(" * On Source-weighted Average option -- Current source-weights are: "+str(source_wgt_dict)),
        
        html.A(
            'Download News Sentiment Data Subset',
            id='download-link',
            download="rawdata.csv",
            href="",
            target="_blank"
        ),
        
    ])

    @app.callback(
        Output("correlation-coef","children"),
        [Input("indicator-name","value"),
        Input("source-name","value"),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')]
    )
    def update_corr(indicator_name, source_name, start_date, end_date):    
        #reference from documentation: https://dash.plotly.com/dash-core-components/datepickerrange


        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')

        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        
        try:
            corr = get_correlation(combined_senti_df, indicators_df.set_index('date'), indicator_name,source_name, start_date=start_date, end_date=end_date)
        except:
            corr = None
        
        string = str(round(corr,2)) if corr else "--"
        
        return "Correlation coeficient between "+indicator_name+ " and selected source sentiment is: "+string 

    @app.callback(
        [Output("indicator-senti-graph","figure"),
        Output("download-link",'href')],# must be a single Output item when returns only one value
        [Input("indicator-name","value"),
        Input("source-name","value"),
        Input("chart-type","value"),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')])
    def update_graph(indicator_name, source_name,chart_type, start_date, end_date):
        
        indicator_colname = 'value_'+"_".join(indicator_name.split())# value_mortgage_rates	
        
        indicator_df = indicators_df[['date', indicator_colname]].dropna().rename(columns={indicator_colname:"values","date":"dates"})
        indicator_label = indic_to_value[indicator_colname]
        test_title = indicator_name + ' VS news sentiment  ' #(most recent 12 months data) 
        
        
        senti_colname = senti_colname_dict[indicator_name]
        
        #filtering by date range
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        
        comb_senti_df = combined_senti_df.sort_index()
        try:
            combo_senti_df = comb_senti_df[start_date:end_date]
        except:
            #for invalid dates, give the full period
            combo_senti_df = comb_senti_df
        
        
        senti_df = combo_senti_df.query('indicator == @senti_colname').drop_duplicates('title_desc')
            
        if source_name == 'Source-weighted Average':
            
            #ref: source_dict = {'Bloomberg': [bbg_gdp_avg, 0.5], 'CBC': [cbc_gdp_avg, 0.5]}
            source_dict = {}
            for src in list(source_wgt_dict.keys()):
                source_df_subset = get_monthly_avg_score(senti_df.query(' source == @src '))
                source_dict[src] = [source_df_subset, source_wgt_dict[src]]
                
            monthly_senti_df = monthly_weighted_average(source_dict)
            month_senti_df = monthly_senti_df.rename(columns={'monthly_weighted_ave_sent_score':'final_sentiment'} )
            
            daily_senti_df = daily_weighted_average(senti_df, source_wgt_dict).rename(columns={'raw_sentiment_score':'final_sentiment'} ) 
            
            
        else:
                
            if source_name != 'All sources':
                senti_df = senti_df.query('source ==@source_name ')
        
            monthly_senti_df =get_monthly_avg_score(senti_df)
            month_senti_df = monthly_senti_df.rename(columns={'monthly_avg_sent_score':'final_sentiment'} ) 
            
            daily_senti_df = senti_df.rename(columns={'raw_sentiment_score':'final_sentiment'} )
        

        if chart_type == 'line':
            chart =  plot_combined_graph_new(indicator_df, month_senti_df, indicator_label, test_title) 

        else:
            chart = plot_combined_graph_scatter(indicator_df, daily_senti_df, indicator_label, test_title)
        
        #export raw sentiment df with column names including "publishedAt","source", "title_desc", "raw sentiment score", "indicator" and "anotation_type"
        csv_string = senti_df.to_csv(encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string)
        
        return chart,csv_string 


    app.run_server(debug=True)
    
    
if __name__ == '__main__':
    indicators_df_path = r'../data/combined_indicator_data.csv'
    senti_df_path = r"../data/combined_sentiment_data.csv"

    main(indicators_df_path, senti_df_path)
    
