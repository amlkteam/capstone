#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Creator: Pandramishi Naga Sirisha
# Created on: 27-05-2020
# Utilities functions to be created into a package


# In[6]:


import pandas as pd
import urllib.request
import json 
from bs4 import BeautifulSoup
import requests
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta, date
import pytz
import dateutil.parser
from collections import defaultdict
import random
import json
import csv
import os


# In[7]:


def convert_json_to_df(project_path,path_to_json):
    """This function reads a json file and outputs a dataframe
    Input:
    ------
    project_path: path to project
    path_to_json: path to json file
    
    Output:
    -------
    Dataframe object
   
   Example:
    project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
    file_path = "project/data_extraction/data/unannotated_data/cbc/interestrates_CBC_article.json"
    converted_df = convert_json_to_df(project_path, file_path)
    """
    if  file_exists(project_path+path_to_json):
        df = pd.read_json(project_path+path_to_json)
        return df
    else:
        print("From convert_json_to_df(): Could not convert the json file to dataframe")
        return None



def check_dir_exists(directory_path):
    """This function check if a given directory exists
    Input:
    ------
    directory_path - string : The path to the directory we want to check
    
    Output:
    --------
    Boolean: True if exists, False if does not exist"""
    
    if  os.path.exists(directory_path):
        return True
    else:
        print("The given path", directory_path, "does not exist")
        return False
    





def file_exists(absolute_file_path):
    """This function check if a given file exists
    Input:
    ------
    absolute_file_path - string : The absolute path to the file we want to check
    
    Output:
    --------
    Boolean: True if exists, False if does not exist"""
    
    if os.path.exists(absolute_file_path):
        return True
    else:
        print("The file:", absolute_file_path, "does not exist")
        return False


# In[10]:


def preprocess_df(df_object,column_name_list,remove_Nans = True):
    """
    This function preprocesses the dataframe
    
    Input:
    ------
    df_object - object: The dataframe object to preprocess
    column_name_list- list: list of required columns
    remove_Nans - Boolean: To remove all rows which contain None or NaN
    filter_query - string
    
    Output:
    -------
    object - The preprocessed dataframe object
    
    Example: preprocess_df(converted_df, ['title', 'description','publishedAt'])
    """
    try:
        subset_columns_df = df_object[column_name_list]
    except:
        print("From preprocess_df(): Check the dataframe object and column names")
        return None
        
    if remove_Nans:
        subset_columns_df = subset_columns_df.dropna()

    return  subset_columns_df
    


def write_df_to_csv(df,project_path,file_path,file_name):
    """Takes a dataframe and writes to a file
    Input:
    ------
    df (Dataframe) - The dataframe to be written to csv
    project_path(String) - The path to the project folder from current folder of from root
    file_path (String) - The path relative to the project_path where to write the file
    file_name (String) - The output file name
    
    Output:
    ------
    File created at : project_path+file_path
    File name:file_name
    """
    if os.path.isdir(project_path+file_path):
        df.to_csv(project_path+file_path+file_name, encoding='utf-8', index=False)
    else:
        print("Path does not exist:", project_path+file_path)
        return None



def sample_dataframe_by_month(dataframe, sample_size):
    """
    create sample of dataframe based on publish date, sample size is the number of articles to be extracted from each month
    Input:
    ------
    dataframe (Dataframe) - The dataframe to be sampled
    sample_size(integer) - The number of articles to be extracted for each month each year
    
    Output:
    -------
    dataframe (Dataframe) - The dataframe after sampling
    """
    article_dictionary_by_month = defaultdict(list)
    full_list = []
    
    if  type(dataframe) is  not pd.DataFrame or not sample_size > 0:
        print("Sample size should be greater than 0")
        return None
    
    try:
        for column, row in dataframe.iterrows():
            article_date = (dateutil.parser.parse(row['publishedAt']))
            article_year = article_date.year
            article_month = article_date.month
            article_dictionary_by_month[str(article_year) + '-' + str(article_month)].append(row)

        for month_number, list_of_articles in article_dictionary_by_month.items():
            random.shuffle(list_of_articles)
            subset_list = list_of_articles[:sample_size]
            full_list.extend(subset_list)

        sample_df = pd.DataFrame(full_list)
        sample_df = sample_df.sort_values(by='publishedAt', ascending=False)
    
    except:
        print("From function sample_dataframe_by_month() : Could not sample")
        return None
    
    return sample_df





def apply_lambda(df, column, lambda_string):
    """Takes a dataframe, column and applies a lambda function to it
    Input:
    ------
    df (Dataframe) - The dataframe to apply the lambda function to
    column (String) - The column name on which to apply the lambda function
    lambda_string (String) - The lambda function code
    
    Output:
    -------
    The dataframe after applying the lambda function
    
    """
    try:
        df[column] = df[column].apply(eval(lambda_string))
        return df    
    except:
        print("Cannot apply lambda function")
        return None




def get_unannotated_data(combined_df, annotated_df, indicator, source, project_path):
    '''This function removes annotated data from all the articles that are collected and gives out the predictions data
    Input:
    -----
    combined_df (Dataframe) - Dataframe containing all the articles
    annotated_df (Dataframe) - Dataframe containing only the sampled articles
    indicator (String) - The economic indicator for the dataframe
    source (String) - The source of the articles cbc/bloomberg
    project_path (String) - the path to the project
    
    Output:
    ------
    Creates file at path: "sentiment_analyzer/data/predictions_data/"
    File name: "predictions_dataset_" + indicator + "_" + source + '.csv'
    '''
    total = combined_df
    drop_list = annotated_df.index.values.tolist()
    total = total.drop(drop_list)
    total['title_desc'] = total['title'] + '. ' + total['description']
    total = total[['source', 'title_desc', 'publishedAt']]
    total = total.drop_duplicates(subset='title_desc', keep='first' )
    
    
    prediction_file_path =  "sentiment_analyzer/data/predictions_data/"
    
    if check_dir_exists(project_path +prediction_file_path + source):
        try:
            prediction_file_path_with_source = prediction_file_path + source + "/"
            prediction_file_name = "predictions_dataset_" + indicator + "_" + source + '.csv'
            write_df_to_csv(total,project_path,prediction_file_path_with_source,prediction_file_name)
        except:
            print("unable to write to file \n")
            return False
        
    if file_exists(project_path+prediction_file_path_with_source+prediction_file_name):
        print("The  number of articles for prediction are ", total.shape[0])
        print("Predictions file generated at :", project_path+prediction_file_path_with_source+prediction_file_name )
        return True
    else:
        print("Final directory is not created \n")
        return False





def get_keyword_df(economic_indicator, project_path,keyword_list, input_file_name,source):
    """
    This function filters a file to find articles containing keywords in the keyword_list
    
    Input:
    ------
    economic_indicator (String) - The economic indicator 
    project_path (String) - The path to the project
    keyword_list (list) - List of keywords to search for in the articles
    input_file_name (String) - Name of the input file which contains articles
    source (String) - The source CBC/Bloomberg
    
    Output:
    -------
    File created at  "sentiment_analyzer/data/predictions_data/<source>"
    File name: "predictions_dataset_<economic_indicator>_<source>.csv
    """
    index_list = set()
    read_file = project_path + "sentiment_analyzer/data/predictions_data/" + source.lower() + "/" + input_file_name
    df = pd.read_csv(read_file, names = ['source','title_desc','publishedAt'],skiprows = 1)
    count = 0
    for  i in range(df.shape[0]):
        text = df.iloc[i]['title_desc']
        found = False
        for keyword in keyword_list:
            if keyword.lower() in text.lower():
                count += 1
                found  = True
        if found == False:
            index_list.add(i)
    predicted_filename = project_path + "sentiment_analyzer/data/predictions_data/" + source.lower() +      "/"+"predictions_dataset_" + economic_indicator + "_" + source.lower() +".csv"
    
    df.drop(df.index[list(index_list)], inplace=True)
    df = df.drop_duplicates('title_desc', keep='last')
    df.to_csv(predicted_filename, index = False)
    print("Total articles retrieved: ", df.shape[0])
    
    
    if file_exists(predicted_filename):
        print("Outputted filtered articles to predict to file :",predicted_filename)
        return True
    else:
        print("Predictions articles after filtering not created")
        return False




def unit_tests():
    project_path = "/non existent"
    file_path = "non_existent_file.json"
    converted_df = convert_json_to_df(project_path, file_path)
    assert converted_df is None, "If path is not present return None"
    
    project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
    file_path = "project/data_extraction/data/unannotated_data/cbc/interestrates_CBC_article.json"
    converted_df = convert_json_to_df(project_path, file_path)
    df = preprocess_df(converted_df, ['xyz'])
    assert df is None
    k = preprocess_df(converted_df, ['title', 'description','publishedAt'])
    assert isinstance(k, pd.DataFrame)
    return True

unit_tests()

