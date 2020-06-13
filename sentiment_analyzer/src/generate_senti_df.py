#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is used to generate one sentiment score for each article
And combine annotated articles and predicted articles into one big dataframe for visualization
"""
import pandas as pd
from datetime import datetime
import sys
import os


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


def combine_annotated_and_predicted(annotation_path, prediction_path, output_path):
    '''combine the both annotated data and predicted data of all sources and 
    all economic indicators into one big dataframe for visualization, each article 
    will have one sentiment score for visualization
    
    inputs:
    dict_annotated_data: dictionary that contains the locations of all annotated data
    dict_unannotated_predictions: dictionary that contains the locations of all predicted data '''
    
    indicators = ['gdp','employment','housing','interest','mortgage','stock']
    
    annotated_list = []
    predicted_list = []
    
    for filename in os.listdir(annotation_path):
        if filename.endswith('.csv'):
            
            df_a = pd.read_csv(annotation_path + filename, parse_dates=['publishedAt'])
            df_a = df_a[['source', 'title_desc','publishedAt', 'title_desc_sent_1']]
            df_a['title_desc_sent_1'] = df_a['title_desc_sent_1'].apply(lambda x: x + 0.5 if x == 1 else (x - 0.5 if x == -1 else x))
            
            for indicator in indicators:
                if indicator in filename.lower():
                    df_a['indicator'] = indicator
                    
            df_a['annotation_type'] = 'annotated'
            df_a = df_a.rename(columns={'title_desc_sent_1':'raw_sentiment_score'}).sort_values(by='publishedAt', ascending=False)
            annotated_list.append(df_a)
            
    annotated_df = pd.concat(annotated_list)
    
    
    for filename in os.listdir(prediction_path):
        if filename.endswith('.csv'):
            df = pd.read_csv(prediction_path + filename, parse_dates=['publishedAt'])
            df['raw_sentiment_score'] = df.apply(lambda row: generate_raw_sentiment_score(row), axis=1)
            df = df[['source', 'title_desc','publishedAt', 'raw_sentiment_score']].sort_values(by='publishedAt', ascending=False)
            
            for indicator in indicators:
                if indicator in filename.lower():
                    df['indicator'] = indicator
                    
            df['annotation_type'] = 'predicted'
            predicted_list.append(df)
    
    predicted_df = pd.concat(predicted_list)
    
    output_df = pd.concat([annotated_df, predicted_df])
    
    # reminded by Amy's code to make all the Bloomberg articles the same source
    output_df.source = output_df.source.str.replace("{'id': 'fp-bloomberg-news', 'name': 'Bloomberg News From FP'}","Bloomberg")
    output_df.source = output_df.source.str.replace("Bloomberg News","Bloomberg")
    output_df.source = output_df.source.str.replace("BNN Bloomberg","Bloomberg")
    # set the index
    output_df = output_df.set_index('publishedAt')
    
    output_df.to_csv(output_path + 'combined_annotation_prediction.csv')
    
    return output_df


annotation_path = '../../data_extraction/data/annotated_data/combined/'
prediction_path = '../data/prediction_output/'
output_path = '../data/prediction_combined/'


combine_annotated_and_predicted(annotation_path, prediction_path, output_path)
assert os.path.exists(output_path + 'combined_annotation_prediction.csv')