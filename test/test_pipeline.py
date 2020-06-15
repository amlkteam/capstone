import sys
import os

# change this module_path to where the parent folder of capstone project scripts is located
module_path = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone'

sys.path.append(module_path)

#from data_extraction.src import scrape_articles_FinancialPost

#output_folder = r'test_fp_data/'

#scrape_articles_FinancialPost.get_BloombergNews_from_FP(2,output_folder)

#scrape_articles_FinancialPost.separate_into_indicator_baskets(output_folder)

##checkpoint: Jun12 8pm -- get_BloombergNews_from_FP() function running.

#assert os.path.exists(output_folder)
#assert os.path.exists(os.path.join(output_folder,'articles_output.json'))
#assert os.path.exists(os.path.join(output_folder,'GDP_output.json'))  


##test model training -- running much slower in this script than in the sentiment_analyzer/src folder

#from sentiment_analyzer.src import Two_stage_flair_training

#if __name__ ==  '__main__':

    #data_folder = os.path.join(module_path,r"sentiment_analyzer/data/annotated_sample_for_training//")

    ## this benchmark_classifier_folder is where the first-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    #benchmark_classifier_folder = r'E:\streamlit_project\gdp_benchmark_classifier\test\\'

    ## here loading in the articles related to GDP from a folder containing oversampled/undersampled train, dev and test splits
    #new_data_folder = os.path.join(module_path,r'sentiment_analyzer/data/oversampled_training_data_combined/GDP//')

    ## this finetuned_classifier_folder is where the second-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    #finetuned_classifier_folder = r'E:\streamlit_project\gdp_finetuned_classifier\test\\'

    #Two_stage_flair_training.main(data_folder,benchmark_classifier_folder,new_data_folder,finetuned_classifier_folder)

##test visualization app -- Jun13 2pm working fine
#assert os.path.exists(data_folder)
#assert os.path.exists(new_data_folder)
#assert os.path.exists(os.path.join(benchmark_classifier_folder,'best-model.pt'))
#assert os.path.exists(os.path.join(finetuned_classifier_folder,'best-model.pt'))

## adding title_desc to hoverinfo in scatter plot for error/correlation analysis (title_desc doesn't exist for "source-weighted Average" option, only applicable for "All sources" and individual source options)



from visualization.src import dash_frontend_final_main

if __name__ ==  '__main__':
    
    indicators_df_path = os.path.join(module_path,r'visualization/data/combined_indicator_data.csv')
    senti_df_path = os.path.join(module_path, r"visualization/data/combined_sentiment_data.csv")

    dash_frontend_final_main.main(indicators_df_path,senti_df_path)

