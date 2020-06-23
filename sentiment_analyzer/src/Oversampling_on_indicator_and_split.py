# -*- coding: utf-8 -*-
"""
@author: Amy Lam

#cleaned and debugged on Jun8
# change export folder structure to be consistent with undersampling function on Jun9
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os



def oversampling_on_indicator_and_split(indicator_file, import_folder, export_folder):
    """takes in a csv file containing mixed-sourced news articles related to a particular economic indicator, 
    performs oversampling on the train_set to make all classes have equal number of examples, then exports the oversampled train csvfile. 
    
    Arguments:
    indicator_file(str) -- the indicator-specific annotation file combining Bloomberg and CBC articles.
    import_folder(path) -- folder that contains the 6 combined annotation files, each file corresponding to one economic indicator.
    export_folder(path) -- folder that will store the oversampled trainset dataframe for training indicator-specific sentiment classifier models.
    
    Returns:
    a train split that is oversampled, a dev split of original dataframe that is not oversampled, and a test split same as dev split.
    
    """
    
    df = pd.read_csv(os.path.join(import_folder,indicator_file), usecols = ['title_desc','title_desc_sent_1','publishedAt'])
    
    ## in the case title and description are not yet combined into one column "title_desc", uncomment below 3 lines
    #df = pd.read_csv(os.path.join(import_folder,indicator_file), usecols = ['title','description','title_desc_sent_1','publishedAt'])
    # add one more column to combine title+description
    #df['title_desc'] = df['title'] + ". " + df['description']

    # do train_test before oversampling to avoid contamination of dev set
    df_train,df_eva = train_test_split(df,test_size = 0.2, random_state = 42)
    df_eva.to_csv(os.path.join(export_folder,'dev.csv'))
    df_eva.to_csv(os.path.join(export_folder,'test.csv'))

    
    #check class imbalance
    #print(df_train['title_desc_sent_1'].value_counts())    

    negative_rows = df_train[df_train['title_desc_sent_1'] == -1]
    neutral_rows =df_train[df_train['title_desc_sent_1'] == 0]
    positive_rows = df_train[df_train['title_desc_sent_1'] == 1]

    ## find the majority class
    majority_label = df_train['title_desc_sent_1'].value_counts().idxmax()
    print(majority_label)
    majority_label_len = df_train['title_desc_sent_1'].value_counts().max()
    print(majority_label_len)

    resampled_rows = []
    for rows in [negative_rows, neutral_rows, positive_rows]:
      resampled = rows.sample(frac = majority_label_len/len(rows),random_state=42,replace=True)
      resampled_rows.append(resampled)


    df_train_oversampled = pd.concat(resampled_rows)

    export_file_path = os.path.join(export_folder,'train.csv')
    df_train_oversampled.to_csv(export_file_path)

#execution 

import_folder = r'../data/annotated_sample_for_training'

## please change indicator names if you're extracting articles associated with other search keywords/other economic indicators
indicator_names = ['gdp','employment','housing','interest_rate','mortgage_rate','stock']
export_names_dict = {'gdp':'gdp','employment':'employment','housing':'housing','interest_rate':'interest_rates','mortgage_rate':'mortgage_rates','stock':'stock_market'}

for indicator_name in indicator_names:
  print(indicator_name)
  indicator_file = 'annotated_'+indicator_name+'_bnn&CBC.csv'

  export_folder = r'../data/oversampled_training_data_combined/'+export_names_dict[indicator_name]
  if not os.path.exists(export_folder):
      os.makedirs(export_folder)

  oversampling_on_indicator_and_split(indicator_file, import_folder, export_folder)

#unit test

assert os.path.exists(r'../data/oversampled_training_data_combined')
assert os.path.exists(r'../data/oversampled_training_data_combined/interest_rates')
assert os.path.exists(r'../data/oversampled_training_data_combined/stock_market/train.csv')
assert os.path.exists(r'../data/oversampled_training_data_combined/stock_market/dev.csv')
assert os.path.exists(r'../data/oversampled_training_data_combined/stock_market/test.csv')
assert os.stat(r'../data/oversampled_training_data_combined/gdp/train.csv').st_size > 0
assert os.stat(r'../data/oversampled_training_data_combined/housing/train.csv').st_size > 0
assert os.stat(r'../data/oversampled_training_data_combined/employment/dev.csv').st_size > 0
assert os.stat(r'../data/oversampled_training_data_combined/mortgage_rates/test.csv').st_size > 0
