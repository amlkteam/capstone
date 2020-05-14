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

base_url = 'https://business.financialpost.com/author/bloombergnp/page/'
endpage = 50

item_dicts = []
for pageno in range(1,endpage):
    
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
        item_dict['source'] = {"id":"fp-bloomberg-news","name":"Bloomberg News From FP"}
        item_dict['author'] = "Bloomberg News" #placeholder value
        item_dict['title'] = item.h4.text.strip().replace("Watch","") # or specifically item.find('h4','gallery-title').text.strip()
        # remove "Watch" for articles with videos
        item_dict['description'] = item.find('div','gallery-mobile-excerpt').text.strip()
        item_dict['url'] = item.a.get('href') #get the first link
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
        item_dict['content'] = article_tree.find('div',"story-content").text.strip()
        
        #done extract, save to item_dicts
        item_dicts.append(item_dict)
    
    print("finished page",pageno)
    time.sleep(3) # pause for 3 seconds before scraping next page
    
### checkpoint: done extraction on one page; len(item_dicts) = 10. record time May12 7:25pm
### checkpoint: done extraction on two pages. 7:43pm
    
## store output as json
output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout'
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
    print(len(indicator_basket),"items inside this indicator basket")
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
