#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Creator: Pandramishi Naga Sirisha
# Created on: 27-05-2020
# Utilities functions to be created into a package


# In[7]:


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


# In[11]:


def convert_json_to_df(project_path,path_to_json):
    """This function reads a json file and outputs a dataframe
    Input:
    ------
    project_path: path to project
    path_to_json: path to json file
    
    Output:
    -------
    Dataframe object
    """
    if  check_dir_exists(project_path+path_to_json):
        df = pd.read_json(project_path+path_to_json)
        return df
    else:
        print("From convert_json_to_df(): Could not convert the json file to dataframe")
        return None

# project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
# file_path = "project/data_extraction/data/unannotated_data/cbc/interestrates_CBC_article.json"
# converted_df = convert_json_to_df(project_path, file_path)


# In[12]:


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
    


# In[13]:


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


# In[155]:


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
    
    """
    try:
        subset_columns_df = df_object[column_name_list]
    except:
        print("From preprocess_df(): Check the dataframe object and column names")
        return None
        
    if remove_Nans:
        subset_columns_df = subset_columns_df.dropna()

    return  subset_columns_df
    
# k = preprocess_df(converted_df, ['title', 'description','publishedAt'])


# In[18]:



def write_df_to_csv(df,project_path,file_path,file_name):
    """Takes a dataframe and writes to a file"""
    if os.path.isdir(project_path+file_path):
        df.to_csv(project_path+file_path+file_name, encoding='utf-8', index=False)
    else:
        print("Path does not exist:", project_path+file_path)
        return None


# In[164]:


def sample_dataframe_by_month(dataframe, sample_size):
    """
    create sample of dataframe based on publish date, sample size is the number of articles to be extracted from each month
    """
    article_dictionary_by_month = defaultdict(list)
    full_list = []
    
    if  type(dataframe) is  not pd.DataFrame or not isinstance(sample_size, int):
        print("not integer")
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


# In[165]:


def apply_lambda(df, column, lambda_string):
    """Takes a dataframe, column and applies a lambda function to it"""
    try:
        df[column] = df[column].apply(eval(lambda_string))
        return df    
    except:
        print("Cannot apply lambda function")
        return None


# In[17]:


def get_unannotated_data(combined_df, annotated_df, indicator, source, prediction_file_path = "../../sentiment_analyzer/data/predictions_data/test/"):
    '''get unannotated data (remove annotated data from all the articles that are collected)'''
    # Running this line will erase current data
    #prediction_file_path = "../../sentiment_analyzer/data/predictions_data/bloomberg/" 
    # try this line for testing
    
    total = combined_df
    drop_list = annotated_df.index.values.tolist()
    total = total.drop(drop_list)
    total['title_desc'] = total['title'] + '. ' + total['description']
    total = total[['source', 'title_desc', 'publishedAt']]
    total = total.drop_duplicates(subset='title_desc', keep='first' )
    #return total
    if check_dir_exists(prediction_file_path):
        total.to_csv(prediction_file_path + 'predictions_dataset_' + indicator + "_" + source + '.csv')
    if file_exists(prediction_file_path + 'predictions_dataset_' + indicator + "_" + source + '.csv'):
        return True
    else:
        print("Final directory is not created")
        return False


# In[169]:


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
    
unit_tests()

