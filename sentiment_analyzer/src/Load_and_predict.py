#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is used to generate prediction results using trained models
User needs to download the model, and specify the directory of the model for prediction
"""

from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings, DocumentRNNEmbeddings, BertEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path
from flair.datasets import CSVClassificationCorpus
from flair.data import Corpus
from flair.data import Sentence
import pandas as pd
import numpy as np
import os

def finetuned_model_predictions(input_file_path, finetuned_classifier, output_file_path):
  '''Makes Sentiment Predictions on unannotated data points contained in the input csvfile by loading the user-defined classifier.
     Exports the csvfile by adding six columns which are best_label, best_confidence(the confidence score for the best label), 
     second_likely (the second likely label), second_confidence (the confidence score for the second likely label) 
     least_likely (the third likely label), and least_confidence (the confidence score for the third likely label) 
     and filling in results from model predictions.
  '''

  unannotated_df = pd.read_csv(input_file_path)
  ## add six new columns to export predictions

  unannotated_df['best_label'] = None
  unannotated_df['best_confidence'] = None
  unannotated_df['second_likely'] = None
  unannotated_df['second_confidence'] = None
  unannotated_df['least_likely'] = None
  unannotated_df['least_confidence'] = None


  for i in range(len(unannotated_df)):

    
    sentence = Sentence(unannotated_df['title_desc'].iloc[i])
    print(sentence)

    finetuned_classifier.predict(sentence, multi_class_prob=True)
    print(sentence)

    pred_score_label = [(sentence.labels[c].score, sentence.labels[c].value) for c in range(len(sentence.labels))]
    print(sentence.labels)
    pred_score_label.sort()

    # list in ascending order on confidence score
    best_label = int(pred_score_label[-1][1])
    best_confidence = pred_score_label[-1][0]
    second_likely_label = int(pred_score_label[-2][1]) 
    second_likely_confidence = pred_score_label[-2][0]
    least_likely_label = int(pred_score_label[0][1]) 
    least_likely_confidence = pred_score_label[0][0]



    unannotated_df['best_label'].iloc[i] = best_label
    unannotated_df['best_confidence'].iloc[i] = best_confidence
    unannotated_df['second_likely'].iloc[i] = second_likely_label
    unannotated_df['second_confidence'].iloc[i] = second_likely_confidence
    unannotated_df['least_likely'].iloc[i] = least_likely_label
    unannotated_df['least_confidence'].iloc[i] = least_likely_confidence



  print(f"All { len(unannotated_df) } rows done prediction! ")

  unannotated_df.to_csv(output_file_path,index=False)

  print("Done export!")
  
  
  
# User should define the data file path used for prediction
#input_file_path = '../data/predictions_data/bloomberg_or_cbc/FILE_NAME'
#output_file_path = '../data/prediction_output/OUT_FILE_NAME'
#classifier = TextClassifier.load('../trained_models/MODEL_NAME')

# test using local files
input_file_path = '../data/predictions_data/bloomberg/predictions_dataset_employment_Bloomberg.csv'
output_file_path = '../data/prediction_output/test_gdp'
classifier = TextClassifier.load('../trained_models/phase_2_employment_model.pt')

finetuned_model_predictions(input_file_path, classifier, output_file_path)

# unit test
assert os.path.exists(output_file_path)
