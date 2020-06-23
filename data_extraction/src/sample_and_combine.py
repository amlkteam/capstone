#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created to generate samples for annotation and use the rest of the articles for prediction
There is also a function to combine the annotated data from both sources, users can call this function
after annotation is finished.
"""

import pandas as pd
from datetime import datetime
import dateutil.parser
from collections import defaultdict
import random
import os

def sample_dataframe_by_month(dataframe, sample_size, keyword):
    """
    create a sample of dataframe based on publish date

    inputs:
    dataframe:    (Pandas.DataFrame) the dataframe to be sampled from
    sample_size: (int) the number of articles to be extracted from each month
    keyword:     (string) should contain the searching query (indicator) used to
                 collect these articles and it's used for naming output file

    outputs:
    CSV file
    (idea is from Sirisha's sample function)
    """

    article_dictionary_by_month = defaultdict(list)
    full_list = []
    output_path = "../data/annotated_data/bloomberg/"
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
    sample_df.to_csv(output_path + keyword + '_sample.csv')
    return sample_df




def combine_fp_bloomberg(bloomberg_json, fp_json):
    '''
    Combine Financial Post articles and Bloomberg articles.
    
    input:
    
    bloomberg_json is the file of articles from bloomberg stored in json format
    fp_json is the the file of articles from financial post stored in json format

    output:
    Pandas DataFrame
    '''
    bloomberg_df = pd.read_json(bloomberg_json)
    bloomberg_df = bloomberg_df[(bloomberg_df.source != 'The Canadian Press') & (bloomberg_df.source != 'Reuters')]
    bloomberg_df = bloomberg_df[bloomberg_df.source.notnull()]
    bloomberg_df['publishedAt'] = bloomberg_df['publishedAt'].apply(lambda x: datetime.strptime(x, '%b %d, %Y').strftime('%Y-%m-%d'))
    
    fp_df = pd.read_json(fp_json)
    fp_df['publishedAt'] = fp_df['publishedAt'].apply(lambda x: ' '.join(x.split()[:3]))
    fp_df['publishedAt'] = fp_df['publishedAt'].apply(lambda x: datetime.strptime(x, '%B %d, %Y').strftime('%Y-%m-%d'))

    concat_df = pd.concat([bloomberg_df, fp_df])
    concat_df.reset_index(drop=True, inplace=True)
    
    # These four columns are created for annotation purpose, they could be commented out or replaced
    concat_df['title_desc_sent_1'] = None
    concat_df['sent_1_note'] = None
    concat_df['title_desc_sent_2'] = None
    concat_df['sent_2_note'] = None
    concat_df = concat_df[['source', 'title', 'description', 'publishedAt']]
    concat_df = concat_df.sort_values(by='publishedAt', ascending=False)
    
    
    
    return concat_df


def get_unannotated_data(combined_df, annotated_df, indicator):
    """
    get unannotated data (remove annotated data from all the articles that are collected)

    inputs:
    combined_df: the dataframe that contains all the articles before sampling
    annotated_df: the dataframe of articles that are sampled for annotation
    indicator: the searching keyword for an economic indicator, in this case only used for naming the output file

    output:
    CSV file
    """
    # Running this line will erase current data
    prediction_file_path = "../../sentiment_analyzer/data/predictions_data/bloomberg/"
    # try this line for testing
    # prediction_file_path = "../../sentiment_analyzer/data/predictions_data/test/"
    
    total = combined_df
    drop_list = annotated_df.index.values.tolist()
    total = total.drop(drop_list)
    total['title_desc'] = total['title'] + '. ' + total['description']
    total = total[['source', 'title_desc', 'publishedAt']]
    total = total.drop_duplicates(subset='title_desc', keep='first' )
    #return total
    total.to_csv(prediction_file_path + 'predictions_dataset_' + indicator + '_Bloomberg.csv')

"""
Run functions to create sample first and then get_unannotated_data function to generate files for prediction
"""
unanno_file_path = "../data/unannotated_data/bloomberg/"
prediction_file_path = "../../sentiment_analyzer/data/predictions_data/bloomberg/"
annotated_output_path = "../data/annotated_data/bloomberg/"

bloomberg_interestrates_comb = combine_fp_bloomberg(unanno_file_path + 'interest_rates_100_Bloomberg_article.json', unanno_file_path + 'interest_rate_fpbloomberg.json')
sample_bloomberg_interestrates = sample_dataframe_by_month(bloomberg_interestrates_comb, 3, 'Bloomberg_interestrates_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_interestrates_combined_sampled.csv')
get_unannotated_data(bloomberg_interestrates_comb, sample_bloomberg_interestrates, 'interestrates')
assert os.path.exists(prediction_file_path + 'predictions_dataset_interestrates_Bloomberg.csv')


bloomberg_housing_comb = combine_fp_bloomberg(unanno_file_path + 'housing_price_100_Bloomberg_article.json', unanno_file_path + 'housing_fpbloomberg.json')
sample_bloomberg_housing = sample_dataframe_by_month(bloomberg_housing_comb, 3, 'Bloomberg_housing_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_housing_combined_sampled.csv')
get_unannotated_data(bloomberg_housing_comb, sample_bloomberg_housing, 'housing')
assert os.path.exists(prediction_file_path + 'predictions_dataset_housing_Bloomberg.csv')

bloomberg_gdp_comb = combine_fp_bloomberg(unanno_file_path + 'GDP_100_Bloomberg_article.json', unanno_file_path + 'GDP_fpbloomberg.json')
sample_bloomberg_gdp = sample_dataframe_by_month(bloomberg_gdp_comb, 3, 'Bloomberg_gdp_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_gdp_combined_sampled.csv')
get_unannotated_data(bloomberg_gdp_comb, sample_bloomberg_gdp, 'GDP')
assert os.path.exists(prediction_file_path + 'predictions_dataset_GDP_Bloomberg.csv')

bloomberg_employment_comb = combine_fp_bloomberg(unanno_file_path + 'employment_95_Bloomberg_article.json', unanno_file_path + 'employment_fpbloomberg.json')
sample_bloomberg_employment = sample_dataframe_by_month(bloomberg_employment_comb, 3, 'Bloomberg_employment_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_employment_combined_sampled.csv')
get_unannotated_data(bloomberg_employment_comb, sample_bloomberg_employment, 'employment')
assert os.path.exists(prediction_file_path + 'predictions_dataset_employment_Bloomberg.csv')

bloomberg_tsx_comb = combine_fp_bloomberg(unanno_file_path + 'stock_market_100_Bloomberg_article.json', unanno_file_path + 'stock_market_fpbloomberg.json')
sample_bloomberg_tsx = sample_dataframe_by_month(bloomberg_tsx_comb, 3, 'Bloomberg_tsx_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_tsx_combined_sampled.csv')
get_unannotated_data(bloomberg_tsx_comb, sample_bloomberg_tsx, 'tsx')
assert os.path.exists(prediction_file_path + 'predictions_dataset_tsx_Bloomberg.csv')

bloomberg_mortgagerates_comb = combine_fp_bloomberg(unanno_file_path + 'mortgage_rates_100_Bloomberg_article.json', unanno_file_path + 'mortgage_rate_fpbloomberg.json')
sample_bloomberg_mortgagerates = sample_dataframe_by_month(bloomberg_mortgagerates_comb, 3, 'Bloomberg_mortgagerates_combined')
assert os.path.exists(annotated_output_path + 'Bloomberg_mortgagerates_combined_sampled.csv')
get_unannotated_data(bloomberg_mortgagerates_comb, sample_bloomberg_mortgagerates, 'mortgagerates')
assert os.path.exists(prediction_file_path + 'predictions_dataset_mortgagerates_Bloomberg.csv')






    
    


    
    
def combine_bnn_cbc(bloomberg_file, cbc_file, out_name):
    """
    combine the annotated bloomberg articles with annotated CBC articles
    """
    bloomberg_df = pd.read_csv(bloomberg_file)
    bloomberg_df = bloomberg_df[['source', 'title', 'description', 'publishedAt', 'title_desc_sent_1']]
    
    CBC_df = pd.read_csv(cbc_file)
    CBC_df.rename(columns = {'date':'publishedAt'}, inplace = True)
    
    concat_df = pd.concat([bloomberg_df,CBC_df])
    concat_df = concat_df.sort_values(by='publishedAt', ascending=False)
    concat_df.reset_index(drop=True, inplace=True)
    concat_df['title_desc'] = concat_df['title'] + '. ' + concat_df['description']
    concat_df = concat_df[['source', 'title_desc', 'publishedAt', 'title_desc_sent_1']]
    
    concat_df.to_csv(out_name + '.csv')