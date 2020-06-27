#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Will be merged with Amy's oversampling function
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os


def undersampling_and_split(import_folder, export_path):
    """
    Takes in a csv file containing mixed-sourced news articles related to a particular economic indicator,
    performs undersampling on the train_set to make all labels have similar number of examples, 
    export the undersampled train, dev, and test csvfile.
    The default export_path is located at sentiment analyzer modele, in undersampled_training_data_combined folder

    """
    
    df = pd.read_csv(import_folder)
    df_non_zero = df[df['title_desc_sent_1'] != 0]
    numof_min_class_bet_pos_neg = df_non_zero['title_desc_sent_1'].value_counts().min()
    
    df_zero = df[df['title_desc_sent_1'] == 0].sample(numof_min_class_bet_pos_neg - 1)
    concat_df = pd.concat([df_non_zero, df_zero])
    concat_df = concat_df[['title_desc', 'publishedAt', 'title_desc_sent_1']]
    
    train, test = train_test_split(concat_df, test_size=0.15, random_state=42)
    
    train.to_csv(export_path + 'train.csv')
    test.to_csv(export_path + 'dev.csv')
    test.to_csv(export_path + 'test.csv')

annotated_data_filepath = '../../data_extraction/data/annotated_data/combined/'
undersampled_path = '../data/undersampled_training_data_combined/'

## please change indicator names if you're extracting articles associated with other search keywords/other economic indicators
indicator_names = ['GDP', 'employment', 'housing', 'interestrates', 'mortgagerates', 'stock']
export_names_dict = {'GDP': 'GDP', 'employment': 'employment', 'housing': 'housing', 'interestrates': 'interest_rates', 'mortgagerates': 'mortgage_rates', 'stock': 'tsx'}

for indicator_name in indicator_names:
    indicator_file = 'annotated_' + indicator_name + '_bnn&CBC.csv'
    export_folder = undersampled_path + export_names_dict[indicator_name]
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
        undersampling_and_split(annotated_data_filepath + indicator_file, export_folder + '/')



## unit tests
assert os.path.exists(undersampled_path)

assert os.path.exists(undersampled_path + 'GDP/')
assert os.path.exists(undersampled_path + 'GDP/train.csv')
assert os.path.exists(undersampled_path + 'housing/dev.csv')
assert os.path.exists(undersampled_path + 'interest_rates/test.csv')

assert os.stat(undersampled_path + 'mortgage_rates/train.csv').st_size > 0
assert os.stat(undersampled_path + 'employment/dev.csv').st_size > 0
assert os.stat(undersampled_path + 'tsx/test.csv').st_size > 0