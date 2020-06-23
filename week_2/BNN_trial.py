# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:18:39 2020

@author: gen80
"""
import requests
from bs4 import BeautifulSoup

search_term = 'GDP'
base_url ='https://www.bnnbloomberg.ca/search/bnn-search-7.337157?q='+search_term+'#/Articles' 


url = 'https://www.bnnbloomberg.ca/search/bnn-search-7.337157?q=GDP#/Articles'
response = requests.get(url)

soup = BeautifulSoup(response.text,'lxml')

#get the section of search results
#soup.find('div','content-main')

articles_tree = soup.find('div',{'id':'Articles'})
feed_items = articles_tree.find_all('li','feed-item') #each <li class="0 feed-item index-N"> tag stores one article, 10 items per page


#digest each item
item_dicts = []
bnn_url = 'https://www.bnnbloomberg.ca'
# need to define null? 
null = None

for item in feed_items:
    
    item_dict = dict()
    item_dict['source'] = {"id":"bnn-bloomberg","name":"BNN Bloomberg"}
    
    item_dict['tags'] = item.find('div','tags').text.strip() #e.g.'\n\n Economics\n\n\n' -> 'Economics'
    item_dict['title'] = item.find('div','article-content').text.strip() #e.g.'Statistics Canada expected to report lower fourth-quarter GDP figures'
    item_dict['url'] = bnn_url + item.find('div','article-content').a.get('href') #e.g. '/statistics-canada-expected-to-report-lower-fourth-quarter-gdp-figures-1.1397341'
    item_dict['urlToImage'] = null # no thumbnail image on Articles search results page
    item_dict['publishedAt'] = item.find('div','date').text.strip() #e.g. 'Feb 28' #need follow-up to normalize data format 
    
    r2 = requests.get(item_dict['url'])
    s2 = BeautifulSoup(r2.text,'lxml')
    article_div = s2.find('div','article')
    item_dict['content'] = article_div.find('div','article-text').text.strip()
    
    article_source = article_div.find('span','source') # text 'The Canadian Press'
    article_author = article_div.find(attrs={'class':'author'}) # None text if story not originated from BNN Bloomberg
    # sometimes author came in as <a class="author">XX</a>
    item_dict['author'] = article_author.text if article_author else article_source.text
    ##?? how to deal with some articles on BNN Bloomberg came from The Canadian Press? discard?
    
    item_dict['description'] = item_dict['content'].split('\n')[0] #get first paragraph of full text
    item_dict['article_fulldate'] = article_div.find('div','date').text.strip() #e.g. 'Feb 28, 2020'
    # article_div.find('div','article-image') this exists in some articles, sometimes replaced by embedded videos
    # get image url: bnn_url + article_div.find('div','article-image').img.get('src')
    
    #done extract, save to item_dicts
    item_dicts.append(item_dict)

### checkpoint: successfully extracted 10 item_dicts. May12 5:41pm
    
### now try to turn the page to get more -- umm hard, frontend created using Angular ng-click/ng-if events


# =============================================================================
# item_dicts[0]
# Out[186]: 
# {'source': {'id': 'bnn-bloomberg', 'name': 'BNN Bloomberg'},
#  'tags': 'Economics',
#  'title': 'Economic growth stalled in February ahead of virus downturn',
#  'url': 'https://www.bnnbloomberg.ca/economic-growth-stalled-in-february-ahead-of-virus-downturn-1.1429383',
#  'urlToImage': None,
#  'publishedAt': 'Apr 30',
#  'content': 'Canada’s economy slid to a halt in February as the COVID-19 outbreak abroad dampened global growth.\nGross domestic product was unchanged from January, missing economist estimates for a 0.1 per cent\xa0gain, Statistics Canada reported Thursday. That follows a 0.2\xa0per cent\xa0jump in the prior month.\nThursday’s numbers don’t provide much insight into the trajectory of the economy since conditions rapidly deteriorated in March when strict social distancing measures took effect. March GDP numbers to be released next month will likely offer greater insight into the extent of the virus on the economy.\n\n\nThe report shows that the Canadian economy was slowing even before the pandemic really hit. Things will get much worse, with Statistics Canada already releasing a “flash” GDP report for March that showed a nine per cent\xa0decline\xa0during the month, and a 2.6\xa0per cent\xa0for the first quarter as a whole.\nRail blockades and labor strikes at schools disrupted economic activity in February with contractions in both the transportation and warehousing sectors and educational services industry\nExcluding the education and transportation sectors, the economy would have posted a 0.2\xa0per cent\xa0gain with 13 of 20 sectors increasing\nInitial impacts of COVID-19 were noticeable in the air transport sector which was down 2.6\xa0per cent\xa0in Feb.\nAccommodation and food services were also impacted by the outbreak, Statistics Canada said\nThe real estate sector was a major contributor to growth, jumping 5.9\xa0per cent\xa0in February\nOn an annual basis, GDP rose 2.1\xa0per cent\nIn a separate release, the agency said the number of payroll employees declined 35,000 in February, led lower by losses in the wholesale trade sector. That’s already the fastest monthly decline since 2015.\nWages were up 3.7 per cent\xa0from a year earlier.\n\n--With assistance from\xa0Erik Hertzberg.',
#  'author': 'Shelly Hagan',
#  'description': 'Canada’s economy slid to a halt in February as the COVID-19 outbreak abroad dampened global growth.',
#  'article_fulldate': 'Apr 30, 2020'}
# =============================================================================



# =============================================================================
# s2.find('div','article')
# Out[146]: 
# <div class="article">
# <header>
# <div class="tags">
# <ul>
# <li class="highlighted"> <h4><a href="      /economics  ">Economics</a></h4>
# </li>
# </ul>
# </div>
# <div class="date">
# <p>        
#                                                             Feb 28, 2020
#                                         </p><p>
# </p></div>
# <div class="headline">
# <h1>Statistics Canada expected to report lower fourth-quarter GDP figures</h1>
# </div>
# <div class="article-info creditWrap">
# <div class="sources"><p><span class="source">The Canadian Press</span></p></div>
# <script>
#                                 var author='The Canadian Press';
#                             </script>
# <ul class="social-right">
# <li>
# <div id="shareBarDiv"></div>
# </li>
# </ul>
# </div>
# <div class="clear"></div>
# </header>
# <div class="article-media enableAutoPlay">
# <div class="article-image">
# <img alt="Canadian dollar loonie $10 bill" height="349" src="/polopoly_fs/1.921584.1511275951!/fileimage/httpImage/image.jpg_gen/derivatives/landscape_620/canadian-dollar-loonie-10-bill.jpg" title="Canadian dollar loonie $10 bill, File photo" width="620"/> </div>
# <div class="byline">
# <p>                            A loonie on a $10 bill
#                         , File photo</p>
# </div>
# </div>
# <script>
#                     var articleText = ".article-text";
#                 </script>
# <div class="article-text"><p>OTTAWA -- The latest reading on the how the Canadian economy fared at the end of last year is due out this morning and it's expected to show that growth slowed to a crawl for the final three months of 2019.</p>
# <p>Statistics Canada is scheduled to release its reading on gross domestic product for December and the fourth quarter.</p>
# <p>Economists on average expect the agency to report that growth in the fourth quarter slowed to an annualized pace of 0.3 per cent, according to financial markets data firm Refinitiv.</p>
# <p>Statistics Canada reported in November that real gross domestic product growth slowed to an annualized rate of 1.3 per cent in the third quarter of last year compared with a reading of 3.5 per cent in the second quarter.</p>
# <p>The GDP report comes amid worries about the impact of the novel coronavirus outbreak that began in China and its impact on the global economy and ahead of an interest rate announcement by the Bank of Canada next week.</p>
# <p>The central bank kept its key interest rate on hold in January, but left the door open to the possibility of rate cuts in the future if weakness in the economy was more persistent than it expected.<br/>
#    <br/>
# </p>
# </div>
# </div>
# =============================================================================






# =============================================================================
# feed_items[0]
# Out[111]: 
# <li class="0 feed-item index-1">
# <article class="article-feed normal $noDate">
# <header>
# <div class="tags">
# <ul>
# <li class="highlighted"> <h4><a href="      /economics  ">Economics</a></h4>
# </li>
# </ul>
# </div>
# <div class="date">
# <p>        
#                                                             Apr 30
#                                         </p><p>
# </p></div>
# </header>
# <div class="headline">
# <div class="article-content">
# <a href="/economic-growth-stalled-in-february-ahead-of-virus-downturn-1.1429383"><h3>Economic growth stalled in February ahead of virus downturn <span class="icon-video"></span></h3></a>
# <div class="clear"></div>
# </div>
# </div>
# </article>
# </li>
# =============================================================================

## explore selenium

# =============================================================================
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# caps = webdriver.DesiredCapabilities.CHROME.copy()
# caps['acceptInsecureCerts'] = True
# driver = webdriver.Chrome(desired_capabilities=caps)
# driver.get("https://www.python.org")
# search_bar = driver.find_element_by_name("q")
# search_bar.send_keys("getting started with python")
# search_bar.send_keys(Keys.RETURN)
# donate_button = driver.find_element_by_class_name("donate-button")
# donate_button.click() ## success transition into a new page! 
# =============================================================================

## ??  /search/bnn-search-tab-view-7.360399/articles-7.360400?ot=example.AjaxPageLayout.ot&q=GDP&q=GDP&parentPaginationAllowed=true&parentMaximumSize=250&parentPageSize=10&pageNum=2'
# =============================================================================
#  <ul class="feed hide-lead">
#  <div id="ajaxCallHolderArticles"></div>
#  <li class="load-more" id="loadmoreboxArticles">
#  <a href="javascript:void(0)" id="loadmoreArticles"><span class="spinner"></span><span>Load More</span></a>
# =============================================================================

## this works!! https://www.bnnbloomberg.ca/search/bnn-search-tab-view-7.360399/articles-7.360400?ot=example.AjaxPageLayout.ot&q=GDP&q=GDP&parentPaginationAllowed=true&parentMaximumSize=250&parentPageSize=10&pageNum=2