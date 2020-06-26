#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is used to generate one sentiment score for each article
And combine annotated articles and predicted articles into one big dataframe for visualization
"""
import pandas as pd
import os


def generate_raw_sentiment_score(row):
    """
    Calculate sentiment score based on best_label.
    
    best_label is the label of the highest confidence score. Its confidence score is best_confidence.
    second_likely is the label of the second highest confidence score. Its confidence score is second_confidence.
    least_likely is the label of the lowest confidence score. Its confidence score is least_confidence.
    
    If an article is predicted as neutral, we use the confidence score of its positive label to minus
    the confidence score of negative label. We use this number to tell whether a certain article is
    slightly positive or slightly negative. If the confidence score of positive and negative are equal
    then we got 0, which means this article is strongly neutral. By doing this we place the range of all
    neutral articles in [-0.5, 0.5].
    
    If an article is predicted as either positive or negative, we first use its label (1 or -1) to multiply 
    its confidence score and then add 0.5 or minus 0.5 to that value. Since the confidence score of neutral 
    prediction will be in the range of [-0.5, 0.5], we do this to prevent positive or negative sentiment scores
    from being in the same range with neutral sentiment scores. 
    
    
    """
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

def get_raw_sentiment_score(row):
    """
    The simplified version of the function above
    Assuming the sentiment analyzer only return the best_label and best_confidence_score,
    under this circumstance the sentiment score of positive prediction would be its confidence score
    the sentiment score of negative prediction would be -1 times its confidence score
    the sentiment score of neutral prediction would be 0

    """
    if row['best_label'] == 1:
        result = row['best_confidence']
    elif row['best_label'] == -1:
        result = -row['best_confidence']
    else:
        result = 0
    return result

def combine_annotated_and_predicted(annotation_path, prediction_path, output_path):
    """
    combine the both annotated data and predicted data of all sources and 
    all economic indicators into one big dataframe for visualization, each article 
    will have one sentiment score for visualization
    
    inputs:
    annotation_path: the path that stores all the annotated datasets
    predicton_path: the path that stores all the predicted datasets
    output_path: the path where the generated csv file will be located
    
    output:
    CSV file
    
    Notice: for annotated articles we assign 1.5 as the sentiment score for
            positive articles and -1.5 as the sentiment score for negative articles.
            For neutral articles, the sentiment score will remain 0.
    """
    
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
    
    # Make sure the source of all Bloomberg articles is the same
    output_df.source = output_df.source.str.replace("{'id': 'fp-bloomberg-news', 'name': 'Bloomberg News From FP'}","Bloomberg")
    output_df.source = output_df.source.str.replace("Bloomberg News","Bloomberg")
    output_df.source = output_df.source.str.replace("BNN Bloomberg","Bloomberg")
    # set the index
    output_df = output_df.set_index('publishedAt')
    
    output_df.to_csv(output_path + 'combined_sentiment_data.csv')
    
    return output_df


annotation_path = '../../data_extraction/data/annotated_data/combined/'
prediction_path = '../data/prediction_output/'
output_path = '../data/prediction_combined/'


combine_annotated_and_predicted(annotation_path, prediction_path, output_path)
assert os.path.exists(output_path + 'combined_sentiment_data.csv')