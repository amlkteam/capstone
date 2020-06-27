#!/usr/bin/env python
# coding: utf-8


import utility_main
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
from dateutil.parser import parse
import os
import datetime


def cbc_sampling_wrapper(economic_indicator,project_path, sample_size,column_names_list = ['title', 'description','publishedAt'],source_string = "cbc", remove_Nans = True):
    """This function creates a sample from a given file  of json 
    Input:
    ------
    economic_indicator (String): The economic indicator
    project_path (String): The path of the project
    sample_size (Integer): The number of articles to sample per month in any year
    column_names_list (list): The list of column names to retain in the final sampled file
    source_string (String): The source (CBC/Bloomberg)"""
    try:
        economic_indicator_list = economic_indicator.split(" ")
        economic_indicator="".join(economic_indicator_list).lower()
        json_file_path =  "data_extraction/data/unannotated_data/" + source_string.upper() + "/" +  economic_indicator + "_" + source_string.upper() + "_article.json"
        print("Reading json file :", project_path + json_file_path + "\n")
        
        df = utility_main.convert_json_to_df(project_path, json_file_path)
        
        preprocessed_df = utility_main.preprocess_df(df,column_names_list)
        preprocessed_df["source"] = source_string
        preprocessed_df = utility_main.apply_lambda(preprocessed_df,'publishedAt' ,"lambda x: x[1]")
        
        sampled_df = utility_main.sample_dataframe_by_month(preprocessed_df, sample_size)
        sampled_df = utility_main.apply_lambda(sampled_df,'publishedAt',"lambda x: dateutil.parser.isoparse(x).date()")
        
        # Write sampled dataframe to data_extraction/data/annotated_data/<source>/<econimc_indicator_sample.csv>
        output_file_path = "data_extraction/data/annotated_data/"  + source_string + "/"
        utility_main.write_df_to_csv(sampled_df,project_path,output_file_path,economic_indicator+"_sample.csv")
        
        
        if utility_main.file_exists(project_path + output_file_path +economic_indicator+"_sample.csv"):
            print("Sample file generated at: ", project_path + output_file_path +economic_indicator+"_sample.csv \n")
            x = utility_main.get_unannotated_data(preprocessed_df, sampled_df, economic_indicator, source_string, project_path)
            if x == True:
                print("Sample and predictions ready \n")
                return True
            else:
                print("Failed to generate predictions file")
                return False
        else:
            print("Could not create the sample file")
    except:
        print("Could not successfully sample the data")
        return False
    


def unit_tests():
    # Testing with wrong project path
    project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/"
    rt = cbc_sampling_wrapper("mortgagerates",project_path, 2,"cbc")
    assert rt == False, "function should return False if wrong file path/name is given"
    
    # Testing with wrong column names
    project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/project/"
    rt = cbc_sampling_wrapper("mortgagerates",project_path,2,['xts', 'description','publishedAt'],"cbc")
    assert rt == False, "function should return False if wrong column names is given"
    # Give wrong sample size
    project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/project/"
    rt = cbc_sampling_wrapper("mortgagerates",project_path, 0, ['title', 'description','publishedAt'],"cbc")
    assert rt == False, "function should return false if sample size is 0 or less"
    print("Successfully passed tests")

unit_tests()


# project_path = "/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/project/"
project_path = "../../../"
cbc_sampling_wrapper("housing",project_path,3)
cbc_sampling_wrapper("mortgage rates",project_path, 3)
cbc_sampling_wrapper("interest rates",project_path, 3)
cbc_sampling_wrapper("gdp",project_path, 3)
cbc_sampling_wrapper("employment",project_path, 3)



# To sample only those articles with given key word use the code below and change parameters
# utility_main.get_keyword_df("mortgagerates",project_path, ["mortgage", "rent", "housing", "interest"], "predictions_dataset_mortgagerates_cbc.csv", "cbc")

