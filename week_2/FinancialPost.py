# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:34:18 2020

@author: gen80
"""

#url = 'https://business.financialpost.com/author/bloombergnp/page/30'

import requests
from bs4 import BeautifulSoup
import time
import os
import json
import csv
import random

base_url = 'https://business.financialpost.com/author/bloombergnp/page/'
endpage = 200
# page 60 dates back to Nov 2019
# page 190 dates back to Nov 2018

item_dicts = []
for pageno in range(147,endpage):
    
    extract_url = base_url+str(pageno)
    
    response = requests.get(extract_url)
    
    soup = BeautifulSoup(response.text,'lxml')
    
    #main text body
    content_section = soup.find('section','author-content')
    feed_items = content_section.find_all('li')
    len(feed_items) # 10 items per page
    
    #None to be replaced by 'null'?  
    
    
    for item in feed_items:
        item_dict = dict()
        
        try:
            item_dict['source'] = {"id":"fp-bloomberg-news","name":"Bloomberg News From FP"}
            item_dict['author'] = "Bloomberg News" #placeholder value
            item_dict['title'] = item.h4.text.strip().replace("Watch","") # or specifically item.find('h4','gallery-title').text.strip()
            # remove "Watch" for articles with videos
            item_dict['description'] = item.find('div','gallery-mobile-excerpt').text.strip()
            item_dict['url'] = item.a.get('href') #get the first link. same as item.a['href']
            item_dict['urlToImage'] = item.img.get('data-src') if item.img else None #some articles has no image
            item_dict['publishedAt'] = item.find('div','post-date').text #e.g. February 24, 2020 10:33 AM EST ##right datetime format?
            item_dict['content'] = item.find('div','gallery-mobile-excerpt').text.strip() #placeholder, not full text
            
            ## go into the url to get full text and author
            article_response = requests.get(item_dict['url'])
            article_soup = BeautifulSoup(article_response.text,'lxml')
            article_tree = article_soup.find('article')
            
            wire_author = article_tree.find('div',"author-container wire-author") # sometimes no journalist name
            main_author = article_tree.find('div',"author-container main-author") # "Bloomberg News"
            item_dict['author'] = wire_author.text.strip() if wire_author else main_author.text.strip()
            paras = article_tree.find('div',"story-content").find_all('p')
            item_dict['content'] = "".join([p.text for p in paras])
        except:
            continue
        
        #done extract, save to item_dicts
        item_dicts.append(item_dict)
    
    print("finished page",pageno)
    time.sleep(3) # pause for 3 seconds before scraping next page
    
### checkpoint: done extraction on one page; len(item_dicts) = 10. record time May12 7:25pm
### checkpoint: done extraction on two pages. 7:43pm

##### for error-proof, should save more often? in case of internet connection lost
##### counter and save within for loop?
    
## store output as json
output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone\week_2\extraction_first200pages_FP_BloombergNews'
article_file = 'articles_output.json'

fout = open(os.path.join(output_folder,article_file),'w')
json.dump(item_dicts,fout) ## dicts wrapped in a list
fout.close()    

## also store csv for training sentiment analyzer?
with open(os.path.join(output_folder,'articles_export.csv'), 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['source','author','title','description','url','urlToImage','publishedAt','content']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for item in item_dicts:
        writer.writerow(item)
        
## separate by 6 economic indicators and store into 6 files
article_file_path = os.path.join(output_folder,article_file)        
f = open(article_file_path, encoding='utf-8')
entries = json.load(f)

#### test one indicator first
GDP_keywords = ['GDP']

def allocate_to_indicator_basket(indicator,indicator_keywords):
    '''takes in a list of search terms related to a particular economic indicator, identify entries that has the search terms and return them.'''
    
    indicator_basket = []
    for entry in entries:
        for kw in indicator_keywords:
            if kw in entry['content']:
                #print(entry['url'])
                indicator_basket.append(entry)
    print(len(indicator_basket),"items inside",indicator,"basket")
    # save in a json file
    fout = open(os.path.join(output_folder, indicator+'_output.json'),'w')
    json.dump(indicator_basket,fout)
    fout.close()
    
    return indicator_basket

GDP_entries = allocate_to_indicator_basket('GDP',GDP_keywords)

### checkpoint: works! May13 6:06pm.  add in other indicators
mortgage_keywords = ['mortgage rates','mortgage'] ## add in more keywords if first keyword cannot return enough entries
interestrate_keywords = ['interest rates']#,'interest rate']
employment_keywords = ['employment']
housing_keywords = ['housing price','housing']
TSX_keywords = ['TSX', 'stock market']

mortgage_entries = allocate_to_indicator_basket('mortgage_rate',mortgage_keywords)
interestrate_entries = allocate_to_indicator_basket('interest_rate',interestrate_keywords)
employment_entries = allocate_to_indicator_basket('employment',employment_keywords)
housing_entries = allocate_to_indicator_basket('housing',housing_keywords)
TSX_entries = allocate_to_indicator_basket('TSX',TSX_keywords)

### checkpoint: 7:31pm for first 50 pages, stats for each of 6 econ indicators
# =============================================================================
# 23 items inside this indicator basket
# 54 items inside this indicator basket
# 47 items inside this indicator basket
# 50 items inside this indicator basket
# 33 items inside this indicator basket
# 78 items inside this indicator basket
# =============================================================================

### checkpoint: 11:20pm done first 200 pages, oldest article before Nov 2018



# =============================================================================
# item_dicts[-1]
# Out[39]: 
# {'source': {'id': 'fp-bloomberg-news', 'name': 'Bloomberg News From FP'},
#  'author': 'Doug Alexander',
#  'title': 'Scotiabank profit tops estimates in revival of capital markets',
#  'description': 'Net income rises 3.5 per cent to $2.33 billion',
#  'url': 'https://business.financialpost.com/news/fp-street/scotiabank-quarterly-profit-tops-estimates-on-strong-markets-unit',
#  'urlToImage': 'https://financialpostcom.files.wordpress.com/2020/02/scotiabank.jpg',
#  'publishedAt': 'February 25, 2020 7:22 AM EST',
#  'content': 'Bank of Nova Scotia’s capital-markets division is showing signs of a turnaround.The unit had long been the weakest link for the Toronto-based lender, with growth in quarterly profit only once in the past two years. The division appears to have turned a corner in the fiscal first quarter, reporting an 11 per cent increase in income, helping the bank post results that beat analysts’ estimates.Key InsightsScotiabank’s global banking and markets division benefited from rising equities and fixed income and more deal activity compared with a year earlier. Earnings for the division totaled $372 million, up from $335 million. The company started reporting global wealth management as a separate division, and business head Glen Gowland wants it to eventually generate 15 per cent of overall bank earnings. Wealth-management earnings rose 12 per cent to $309 million, to account for 13 per cent of overall earnings. Scotiabank has exited more than 20 countries in the past six years, scaling back in the Caribbean and Asia to focus on the Americas, with an emphasis on Mexico, Peru, Chile and Colombia. The international-banking division earned $582 million, down 30 per cent from $828 million a year earlier. The lender told investors in January that it aims to get 40 per cent of its earnings from Canadian banking. The domestic-banking division had earnings of $852 million in the first quarter, down 1 per cent from a year ago. Market ReactionScotiabank has fallen 0.3 per cent this year through Monday, underperforming the 2.2 per cent gain for Canada’s eight-company S&P/TSX Commercial Banks Index.Get MoreNet income for the three months through Jan. 31 rose 3.5 per cent to $2.33 billion, or $1.84 a share, after a gain from its Thanachart Bank sale, charges tied to derivatives and discontinued software, and revisions to its allowance for credit losses. Adjusted earnings totaled $1.83 a share, beating the $1.75 estimate of 13 analysts in a Bloomberg survey. Bloomberg.com'}    
# =============================================================================
    
    

# =============================================================================
# feed_items[-1]
# Out[10]: 
# <li>
# <article class="post post-excerpt hentry track_event top-headline show-look-label commodities" data-event-tracking="Sidebar Outfit|0|author|0||author|author|||Bloomberg News||">
# <figure class="thumbnail">
# <a href="https://business.financialpost.com/commodities/energy/teck-pulls-application-for-oil-sands-mine-in-relief-for-trudeau" id="link-1986809" target="">
# <img alt="" class="attachment-post-thumbnail wp-post-image hide-on-video-play" data-src="https://financialpostcom.files.wordpress.com/2020/02/teck-resources-1.jpg" height="750" id="img-1986809" itemprop="image" src="https://financialpostcom.files.wordpress.com/2020/02/teck-resources-1.jpg" width="1000"/>
# </a>
# </figure>
# <header>
# <h4 class="gallery-title"><a href="https://business.financialpost.com/commodities/energy/teck-pulls-application-for-oil-sands-mine-in-relief-for-trudeau" rel="bookmark" target="" title="">Teck Resources pulls Frontier oilsands mine project, blaming divisive debate over climate change</a></h4> </header>
# <div class="entry-content gallery-details">
# <div class="post-author">
# 			Bloomberg News			</div>
# <div class="post-date">February 23, 2020 10:15 PM EST</div>
# <div class="gallery-excerpt">
# <div class="entry-content gallery-mobile-excerpt">
# 				For Alberta, which has struggled with the downturn in oil prices since 2014, Frontier would have been a boon				</div>
# </div>
# </div>
# </article>
# </li>
# =============================================================================


# =============================================================================
# #combining different webscrap batches
# 
# def combine_batches_per_indicator(indicator_name):
#     
#     '''Combine extractions of batches of pages extraction according to name of each economic indicator'''
# 
#     folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout'
#     folder2 = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout\page50-118'
#     folder3 = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout\page119-200'
#     
#     file = indicator_name +'_output.json'
#     f = open(folder+'/'+file,encoding='utf-8')
#     entries = json.load(f)
#     f.close()
#     
#     f = open(folder2+'/'+file,encoding='utf-8')
#     entries2 = json.load(f)
#     f.close()
#     
#     f = open(folder3+'/'+file,encoding='utf-8')
#     entries3 = json.load(f)
#     f.close()
#     
#     entries.extend(entries2)
#     entries.extend(entries3)
#     
#     print(len(entries))
#     
#     output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone\week_2\extraction_first200pages_FP_BloombergNews'
#     article_file = indicator_name +'_output.json'
#     fout = open(os.path.join(output_folder,article_file),'w')
#     json.dump(entries,fout) ## dicts wrapped in a list
#     fout.close()
#     
#     return entries
# 
# GDP_entries = combine_batches_per_indicator('GDP')
# employment_entries = combine_batches_per_indicator('employment')
# housing_entries = combine_batches_per_indicator('housing')
# interest_rate_entries = combine_batches_per_indicator('interest_rate')
# mortgage_rate_entries = combine_batches_per_indicator('mortgage_rate') ## strange-- some duplicates, 160 unique values -- deal with when reading in pandas
# TSX_entries = combine_batches_per_indicator('TSX')
# 
# #all articles combined
# articles_entries = combine_batches_per_indicator('articles')
# =============================================================================
# =============================================================================
# 
# ## get random samples for annotations
# def load_entries(indicator_name):
#     folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone\week_2\extraction_first200pages_FP_BloombergNews'
#     file = indicator_name +'_output.json'
#     f = open(folder+'/'+file,encoding='utf-8')
#     entries = json.load(f)
#     f.close()
#     return entries
# 
# 
# def random_sampling(indicator_name,target_number=50):
#     '''takes in an economic indicator's name, get the list containing json-format info of articles related to the indicator.
#     returns a random sample of target size and save as csv file for annotation use.'''
#     
#     sample = []
#     added_url = set()
#     
#     entries = load_entries(indicator_name)
#     
#     while len(sample) < target_number:
#         entry = random.choice(entries)
#         # to prevent duplicate entries. treat url as unique article ID
#         if entry['url'] not in added_url:
#             sample.append(entry)
#             added_url.add(entry['url'])
#     # reached desired sample size, save to file for annotation
#     # change output_folder below. assuming same folder for all samples of different indicators
#     output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout\annotations_50'
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#     
#     with open(os.path.join(output_folder,indicator_name+"_"+str(target_number)+'_annotations.csv'), 'a', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['source','author','title','description','url','urlToImage','publishedAt','content']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for item in sample:
#             writer.writerow(item)
#         
#     return sample
#     
# #use case
# GDP_entries = load_entries('GDP')
# housing_sample = random_sampling('GDP')
# 
# employment_sample = random_sampling('employment')
# housing_sample = random_sampling('housing')
# interest_rate_sample = random_sampling('interest_rate')
# mortgage_rate_sample = random_sampling('mortgage_rate')
# TSX_sample = random_sampling('TSX')
# 
# =============================================================================

##Below written by Aaron
import pandas as pd
from collections import defaultdict
import dateutil.parser
from datetime import datetime, timedelta
import re

def sample_dataframe_by_month(dataframe, sample_size):
    """
    create sample of dataframe based on publish date, sample size is the number of articles to be extracted from each month
    """
    article_dictionary_by_month = defaultdict(list)
    full_list = []
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
    return sample_df

def combine_fp_bloomberg_then_sample(bloomberg_json, fp_json, keyword, article_num_per_month):
    '''
    Combine financial post articles and bloomberg articles, and create a sample by publish date.
    
    input:
    
    bloomberg_json is the file of articles from bloomberg stored in json format
    fp_json is the the file of articles from financial post stored in json format
    keyword is the searching query used to collect these articles
    
    '''
    bloomberg_df = pd.read_json(bloomberg_json)
    bloomberg_df = bloomberg_df.drop_duplicates('url')
    #bloomberg_df = bloomberg_df[(bloomberg_df.source != 'The Canadian Press') & (bloomberg_df.source != 'Reuters')]
    bloomberg_df = bloomberg_df[(bloomberg_df.source == 'Bloomberg News')]
    bloomberg_df = bloomberg_df[bloomberg_df.source.notnull()]
    bloomberg_df['publishedAt'] = bloomberg_df['publishedAt'].apply(lambda x: datetime.strptime(x, '%b %d, %Y').strftime('%Y-%m-%d'))
    
    fp_df = pd.read_json(fp_json)
    fp_df = fp_df.drop_duplicates('url')
    fp_df['publishedAt'] = fp_df['publishedAt'].apply(lambda x: ' '.join(x.split()[:3]))
    fp_df['publishedAt'] = fp_df['publishedAt'].apply(lambda x: datetime.strptime(x, '%B %d, %Y').strftime('%Y-%m-%d'))

    concat_df = pd.concat([bloomberg_df, fp_df])
    concat_df.reset_index(drop=True, inplace=True)
    
    concat_df['title_desc_sent_1'] = None
    concat_df['sent_1_note'] = None
    concat_df['title_desc_sent_2'] = None
    concat_df['sent_2_note'] = None
    concat_df = concat_df[['source', 'author', 'title', 'description', 'title_desc_sent_1', 'sent_1_note', 'title_desc_sent_2', 'sent_2_note', 'publishedAt', 'url', 'urlToImage', 'content']]
    
    sample_df = sample_dataframe_by_month(concat_df, article_num_per_month)
    
    sample_df.to_csv(keyword + '_sample.csv')
    
    return len(sample_df)

# =============================================================================
# combine_fp_bloomberg_then_sample(bnn_folder+bloomberg_json, fp_folder+fp_json, 'stock_market_combined', 3)
# combine_fp_bloomberg_then_sample(bnn_folder+'employment_95_Bloomberg_article.json', fp_folder+'employment_output.json', 'employment_combined', 3)
# combine_fp_bloomberg_then_sample(bnn_folder+'GDP_100_Bloomberg_article.json', fp_folder+'GDP_output.json', 'GDP_combined', 3)
#     
# =============================================================================
# Using Ajax Api to scrape Bloomberg Articles

def clean_bloomberg_date(date):
    'convert the date of articles to month(abbreviated) day, year'
    if not "ago" in date: # if the original date format of bloomberg post is XXX hours ago
        new_date = date
    else:
        hrs = re.search("\d+", date) #regex extracts the time in hours
        new_date = (datetime.now() - timedelta(hours=int(hrs.group()))) #calculates the date when the post was created
        new_date = datetime.strftime(new_date, '%b %d, %Y')
    return new_date

def bnn_article_scraper(query):
    '''
    Srape the article news from BNN Bloomberg website with a search query
    Return a json file containing the returned articles
    
    input:
    query: (str) search keyword
    '''
    output_list = []
    search_query = 'q=' + '&q='.join(query.split())
    url_prefix = 'https://www.bnnbloomberg.ca'
    url = f'https://www.bnnbloomberg.ca/search/bnn-search-tab-view-7.360399/articles-7.360400?ot=example.AjaxPageLayout.ot&{search_query}&parentPaginationAllowed=false'

    response = requests.get(url)
    api_soup = BeautifulSoup(response.text, 'lxml')
    
    for article in api_soup.find_all('div', {'class': 'article-content'}):
        
        try:
            title = article.a.text.strip()
            #print("article_title:", title)
    
            article_url = url_prefix + article.a.get('href').strip()
            #print("article_url:", article_url)
    
    
    
            article_response = requests.get(article_url)
            article_soup = BeautifulSoup(article_response.text, 'lxml')
            # get date
            date_tag = article_soup.find('div', class_ = "date")
            if date_tag:
                date = date_tag.get_text().strip()
            else:
                date = None
            #print('date:', date)
    
            # get author
            author_tag = article_soup.find('span', class_ = "author")
            if author_tag:
                author = author_tag.get_text().strip()
            else:
                author = None 
            #print('author:', author)
    
            # get source
            source_tag = article_soup.find('span', {'class':'source'})
            if source_tag:
                source = source_tag.get_text().strip()
            else:
                source = None
            #print('source:', source)
    
            # get content
            article_text_tag = article_soup.find('div', {'class':'article-text'})
            if article_text_tag:
                article_text = article_text_tag.get_text(' ')
                desc = article_text_tag.text.strip().split("\n")[0]
            else:
                article_text_tag = article_soup.find('div', {'class':'article-text-chart'})
                if article_text_tag:
                    article_text = article_text_tag.get_text(' ')
                    desc = article_text_tag.text.strip().split("\n")[0]
                else:
                    article_text = None
                    desc = None
            #print('content:', article_text)
    
            # get image url
            article_image_tag = article_soup.find('p', {'class':'image-center'})
            if article_image_tag:
                image_url = url_prefix + article_image_tag.img['src']
            else:
                image_url = None
            #print('image_url:', image_url)
            #print('\n')
            
            article_dict = {}
            
            article_dict['source'] = source
            article_dict['author'] = author
            article_dict['title'] = title
            article_dict['description'] = desc
            article_dict['url'] = article_url
            article_dict['urlToImage'] = image_url
            article_dict['publishedAt'] = clean_bloomberg_date(date)
            article_dict['content'] = article_text
        except:
            continue
        
        output_list.append(article_dict)
        
    output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\better_dwelling_capstone\week_2\BNN_extractions_6indicators'
    filename = '_'.join(query.split()) + '_' + str(len(output_list)) + '_' +'Bloomberg_article' + '.json'
    with open(os.path.join(output_folder, filename), 'w') as json_file:
        json.dump(output_list, json_file)
        
    return output_list

bloomberg_mr_article = bnn_article_scraper('mortgage rates')
bloomberg_ir_article = bnn_article_scraper('interest rates')
bloomberg_hp_article = bnn_article_scraper('housing price')
bloomberg_e_article = bnn_article_scraper('employment')
bloomberg_gdp_article = bnn_article_scraper('GDP')
bloomberg_tsx_article = bnn_article_scraper('stock market')
