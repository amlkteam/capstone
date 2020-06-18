#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Will be merged with Amy's oversampling function
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os


def undersampling_and_split(import_folder, export_path):
    '''takes in a csv file containing mixed-sourced news articles related to a particular economic indicator, 
    performs undersampling on the train_set to make all labels have similar number of examples, 
    export the undersampled train, dev, and test csvfile. '''
    
    df = pd.read_csv(import_folder)
    df_non_zero = df[df['title_desc_sent_1'] != 0]
    numof_min_class_bet_pos_neg = df_non_zero['title_desc_sent_1'].value_counts().min()
    
    df_zero = df[df['title_desc_sent_1'] == 0].sample(numof_min_class_bet_pos_neg - 1)
    concat_df = pd.concat([df_non_zero, df_zero])
    #print(concat_df['title_desc_sent_1'].value_counts())
    
    train, test = train_test_split(concat_df, test_size=0.15, random_state=42)
    
    train.to_csv(export_path + 'train.csv')
    test.to_csv(export_path + 'dev.csv')
    test.to_csv(export_path + 'test.csv')

annotated_data_filepath = '../../data_extraction/data/annotated_data/combined/'
undersampled_path = '../data/phase_2_training/Undersampled_data/'

undersampling_and_split(annotated_data_filepath + 'annotated_GDP_bnn&CBC.csv', undersampled_path + 'GDP/')
undersampling_and_split(annotated_data_filepath + 'annotated_housing_bnn&CBC.csv', undersampled_path + 'housing/')
undersampling_and_split(annotated_data_filepath + 'annotated_interestrates_bnn&CBC.csv', undersampled_path + 'interest_rates/')
undersampling_and_split(annotated_data_filepath + 'annotated_mortgagerates_bnn&CBC.csv', undersampled_path + 'mortgage_rates/')
undersampling_and_split(annotated_data_filepath + 'annotated_employment_bnn&CBC.csv', undersampled_path + 'employment/')
undersampling_and_split(annotated_data_filepath + 'annotated_tsx_bnn&CBC.csv', undersampled_path + 'tsx/')

## unit tests
assert os.path.exists(undersampled_path)

assert os.path.exists(undersampled_path + 'GDP/')
assert os.path.exists(undersampled_path + 'GDP/train.csv')
assert os.path.exists(undersampled_path + 'housing/dev.csv')
assert os.path.exists(undersampled_path + 'interest_rates/test.csv')

assert os.stat(undersampled_path + 'mortgage_rates/train.csv').st_size > 0
assert os.stat(undersampled_path + 'employment/dev.csv').st_size > 0
assert os.stat(undersampled_path + 'tsx/test.csv').st_size > 0