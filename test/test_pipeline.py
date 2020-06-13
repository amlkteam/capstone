import sys
import os

# change this module_path to where the parent folder of capstone project scripts is located
module_path = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone'

sys.path.append(module_path)

from data_extraction.src import scrape_articles_FinancialPost

output_folder = r'test_fp_data/'

scrape_articles_FinancialPost.get_BloombergNews_from_FP(2,output_folder)

scrape_articles_FinancialPost.separate_into_indicator_baskets(output_folder)

##checkpoint: Jun12 8pm -- get_BloombergNews_from_FP() function running.

assert os.path.exists(output_folder)
assert os.path.exists(os.path.join(output_folder,'articles_output.json'))
assert os.path.exists(os.path.join(output_folder,'GDP_output.json'))   

