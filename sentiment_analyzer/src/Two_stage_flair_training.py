# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:22:17 2020

@author: Amy(.py wrapper), Aaron(original code from his Google Colab notebook)

#checkpoint: Jun8 swapped to relative path
#checkpoint: Jun8 11:31pm cleared bugs for running training in local machine
#Please use flair version 0.5

#below a demo for training a finetuned classifier for GDP-related articles

#please check our indicator-specific model finetuning results corresponding to each of the 6 economic-indicators in the .ipynb Notebooks inside this folder.
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# many future warnings related to tensorflow
 
def main(data_folder,benchmark_classifier_folder,new_data_folder,finetuned_classifier_folder):
    from flair.embeddings import FlairEmbeddings, DocumentLSTMEmbeddings, BertEmbeddings, DocumentRNNEmbeddings, TransformerDocumentEmbeddings
    from flair.models import TextClassifier
    from flair.trainers import ModelTrainer
    from flair.datasets import CSVClassificationCorpus
    from flair.data import Corpus
    import pandas as pd
    import os
    

    
    ### First Stage (Train on benchmark dataset)
    benchmark = pd.read_csv(data_folder+"combined_benchmark.csv")
    benchmark = benchmark[['label', 'text']]
    
    #### Create train, dev and test set
    #benchmark = benchmark.sample(frac=1) # if not set random state, everytime has different training result
    benchmark = benchmark.sample(frac=1, random_state=42)
    benchmark.iloc[0:int(len(benchmark)*0.8)].to_csv(data_folder + 'train.csv', sep='\t', index = False, header = False)
    benchmark.iloc[int(len(benchmark)*0.8):int(len(benchmark)*0.9)].to_csv(data_folder + 'test.csv', sep='\t', index = False, header = False)
    benchmark.iloc[int(len(benchmark)*0.9):].to_csv(data_folder + 'dev.csv', sep='\t', index = False, header = False)
    
    #### Build corpus
    column_name_map = {1: "text", 0: "label_topic"}
    
    corpus: Corpus = CSVClassificationCorpus(data_folder,
                                             column_name_map,
                                             skip_header=False, #no header in kaggle data
                                             delimiter='\t',    # comma separated rows
                                             #train_file='train.csv', ## passing in file names manually when it can't auto detect
                                             #dev_file='dev.csv',
                                             #test_file='test.csv'
    )
    
    #### Create word embeddings
    word_embeddings = [BertEmbeddings(), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
    ## caveat: issue of deprecation. BertEmbeddings and DocumentLSTMEmbeddings existed in version 0.4.5, and became legacy embeddings(still available) in version 0.5
    
    #### First Stage Fine-tuning
    document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)
    classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)
    trainer = ModelTrainer(classifier, corpus)
    #trainer.train(benchmark_classifier_folder, max_epochs=1) #offline test use epoch=1
    trainer.train(benchmark_classifier_folder, max_epochs=10)
    
    ### every finetuning results in different scores
    ### accuracy at phase1 finetuning does not matter too much, phase2 scores more important in biasing the models towards learning indicator-specific keywords
    
    ### Second Stage (train on hand annotated datasets)
    #### Build corpus
    
    
    ### this column_name_map must be updated to reflect which column stores the X(text features) and y(golden labels) for training use
    ### in the csv file contained in new_data_folder, 2nd column is 'title_desc',
    ### 4th column is 'title_desc_sent_1' (where we stored agreed sentiment annotations)
    new_column_name_map = {1: "text", 3: "label_topic"}
    print(new_column_name_map)
    
    corpus: Corpus = CSVClassificationCorpus(new_data_folder,
                                             new_column_name_map,
                                             skip_header=True, 
                                             delimiter=','    # comma separated rows
    )
     
    #### Second Stage fine-tuning
    
    benchmark_classifier = TextClassifier.load(os.path.join(benchmark_classifier_folder,'best-model.pt'))
    trainer = ModelTrainer(benchmark_classifier, corpus)
    #trainer.train(finetuned_classifier_folder, max_epochs=1) #offline test use
    trainer.train(finetuned_classifier_folder, max_epochs=10) 
    
    
    #### load the 2nd-stage finetuned model for prediction:
    ## finetuned_classifier = TextClassifier.load(os.path.join(finetuned_classifier_folder,'best-model.pt'))


if __name__ ==  '__main__':

    data_folder = r"../data/annotated_sample_for_training//"

    ## this benchmark_classifier_folder is where the first-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    benchmark_classifier_folder = r'../trained_models/gdp_benchmark_classifier//'

    ## here loading in the articles related to GDP from a folder containing oversampled/undersampled train, dev and test splits
    new_data_folder = r'../data/oversampled_training_data_combined/GDP//'

    ## this finetuned_classifier_folder is where the second-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    finetuned_classifier_folder = r'../trained_models/gdp_finetuned_classifier//'

    main(data_folder,benchmark_classifier_folder,new_data_folder,finetuned_classifier_folder)









