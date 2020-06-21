# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:34:18 2020

@author: Amy Lam
## June14: added multithreading
"""

import requests
from bs4 import BeautifulSoup
import time
import os
import json
import csv
import random
import threading


def get_BloombergNews_from_FP(startpage,endpage,outputs):
    """
    extracts latest articles from the author "Bloomberg News" from Financial Post website.
    Most recent articles are on top and each page contains 10 articles.  
    
    Arguments:
    startpage(int) -- the page number to start scraping
    endpage(int) -- the final page number to scrape
    outputs(list) -- a list where multithreading processes are storing the output from this function.
    
    """

    base_url = 'https://business.financialpost.com/author/bloombergnp/page/'
    # page 60 dates back to Nov 2019
    # page 190 dates back to Nov 2018
    
    item_dicts = []
    for pageno in range(startpage,endpage):
        
        extract_url = base_url+str(pageno)
        
        response = requests.get(extract_url)
        
        soup = BeautifulSoup(response.text,'lxml')
        
        #main text body
        content_section = soup.find('section','author-content')
        feed_items = content_section.find_all('li')
        # 10 items per page
        
        
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
        
        outputs[int(startpage/20)]=item_dicts
        

def BloombergNews_from_FP(endpage, output_folder):
    '''
    A multithreading extraction execution of get_BloombergNews_from_FP() function to save time. Extracts 20 pages in a single thread.
    
    Arguments:
    endpage(int) -- the first n-th pages to extract.
    output_folder(path) -- a folder to export all the extracted article infos in a JSON file and a CSV file.
    
    '''
    #reference: <<Automate the boring stuff with Python>> Chapter 15

    downloadThreads = []
    outputs = [None] * int(endpage/20)
    for i in range(0,endpage,20):
        downloadThread = threading.Thread(target=get_BloombergNews_from_FP, args=(i,i+20,outputs))
        downloadThreads.append(downloadThread)
        downloadThread.start()
        
    for downloadThread in downloadThreads:
        downloadThread.join()
    print('Done extraction.') ## this narrows down the execution time of scraping 
           
    all_itemdicts = [d for o in outputs for d in o]
    #print(len(all_itemdicts))
    os.makedirs(output_folder,exist_ok=True)
    
    ## store output as json
    article_file = 'articles_output.json'
    
    fout = open(os.path.join(output_folder,article_file),'w')
    json.dump(all_itemdicts,fout) ## dicts wrapped in a list
    fout.close()    
    
    ## also store csv for training sentiment analyzer
    with open(os.path.join(output_folder,'articles_export.csv'), 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source','author','title','description','url','urlToImage','publishedAt','content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in all_itemdicts:
            writer.writerow(item)

     

def allocate_to_indicator_basket(entries,indicator,indicator_keywords,output_folder):
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



    
#### separate by 6 economic indicators and store into 6 files

def separate_into_indicator_baskets(output_folder):

    """
    defines keywords for each economic indicator and calls the allocate_to_indicator_basket() function for each of the six selected economic indicators. Exports to JSON files in the user-defined output_folder.

    Argument:
    output_folder(path) -- a folder to store the six indicator-specific articles in JSON format.

    """
    article_file = 'articles_output.json'
    article_file_path = os.path.join(output_folder,article_file)        
    f = open(article_file_path, encoding='utf-8')
    entries = json.load(f)
    f.close()
    
    ## add in more keywords if first keyword cannot return enough entries. caveat: may lead to inclusion of many irrelevant articles and affect model training result and correlation calculation
    GDP_keywords = ['GDP']
    mortgage_keywords = ['mortgage rates']#,'mortgage'] 
    interestrate_keywords = ['interest rates']#,'interest rate']
    employment_keywords = ['employment']
    housing_keywords = ['housing price']#,'housing']
    TSX_keywords = ['TSX']#, 'stock market']

    GDP_entries = allocate_to_indicator_basket(entries,'GDP',GDP_keywords,output_folder)
    mortgage_entries = allocate_to_indicator_basket(entries,'mortgage_rate',mortgage_keywords,output_folder)
    interestrate_entries = allocate_to_indicator_basket(entries,'interest_rate',interestrate_keywords,output_folder)
    employment_entries = allocate_to_indicator_basket(entries,'employment',employment_keywords,output_folder)
    housing_entries = allocate_to_indicator_basket(entries,'housing',housing_keywords,output_folder)
    TSX_entries = allocate_to_indicator_basket(entries,'TSX',TSX_keywords,output_folder)

####execution of functions here
##uncomment the line below to execute extract or separation function   
##output_folder = '../data/unannotated_data/bloomberg/extraction_first200pages_FP_BloombergNews'

##uncomment the line below to execute extract function 
#BloombergNews_from_FP(200,output_folder)   

##uncomment the line below to execute separation function 
#separate_into_indicator_baskets(output_folder)

##tests
#assert os.path.exists(output_folder)
#assert os.path.exists(os.path.join(output_folder,'articles_output.json'))
#assert os.path.exists(os.path.join(output_folder,'GDP_output.json')) 

#### examples of one extraction
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
    
    
#### example of original article display in html tags
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
