"""
# Code that is used to scrape articles from bnn bloomberg archive
# This script will allow users to scrape 100 previous articles from the bnn bloomberg website for each searching query from the date when the code is executed
# Code can be improved 
"""

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime, timedelta
import re


def clean_bloomberg_date(date):
    """
    convert the date of articles to month(abbreviated) day, year
    """
    if date is None:
        new_date = None
    elif "ago" not in date:  # if the original date format of bloomberg post is XXX hours ago
        new_date = date
    else:
        hrs = re.search("\d+", date)  # regex extracts the time in hours
        new_date = (datetime.now() - timedelta(hours=int(hrs.group())))  # calculates the date when the post was created
        new_date = datetime.strftime(new_date, '%b %d, %Y')
    return new_date


def bnn_article_scraper(query, out_path):
    """
    Srape the article news from BNN Bloomberg website with a search query
    Return a json file containing the returned articles
    
    input:
    query: (str) search keyword
    out_path: (str) the file path where the file of the scraped articles will be located
    """
    print("Scraping " + query + " ... ")
    output_list = []
    search_query = 'q=' + '&q='.join(query.split())
    url_prefix = 'https://www.bnnbloomberg.ca'
    url = f'https://www.bnnbloomberg.ca/search/bnn-search-tab-view-7.360399/articles-7.360400?ot=example.AjaxPageLayout.ot&{search_query}&parentPaginationAllowed=false'

    response = requests.get(url)
    api_soup = BeautifulSoup(response.text, 'lxml')

    for article in api_soup.find_all('div', {'class': 'article-content'}):

        title = article.a.text.strip() if article.a else None
        # print("article_title:", title)

        article_url = url_prefix + article.a.get('href').strip()
        # print("article_url:", article_url)

        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'lxml')

        # get date
        date_tag = article_soup.find('div', class_="date")
        date = date_tag.get_text().strip() if date_tag else None
        # print('date:', date)

        # get author
        author_tag = article_soup.find('span', class_="author")
        author = author_tag.get_text().strip() if author_tag else None
        # print('author:', author)

        # get source
        source_tag = article_soup.find('span', {'class': 'source'})
        source = source_tag.get_text().strip() if source_tag else None
        # print('source:', source)

        # get content
        article_text_tag = article_soup.find('div', {'class': 'article-text'})
        article_text = ''

        if article_text_tag:
            for children in article_text_tag:
                # print(children)
                if children.name == 'p':
                    article_text += ' ' + children.text
            # article_text = article_text_tag.text
            # desc = article_text_tag.p.get_text()
            desc = article_text_tag.text.strip().split("\n")[0]
        else:
            article_text_tag = article_soup.find('div', {'class': 'article-text-chart'})
            if article_text_tag:
                for children in article_text_tag:
                    if children.name == 'p':
                        article_text += ' ' + children.text
                # article_text = article_text_tag.get_text(' ')
                # desc = article_text_tag.p.get_text()
                desc = article_text_tag.text.strip().split("\n")[0]  
            else:
                article_text = None
                desc = None
        # print('content:', article_text)

        # get image url
        article_image_tag = article_soup.find('p', {'class': 'image-center'})
        image_url = url_prefix + article_image_tag.img['src'] if article_image_tag else None



        article_dict = {}

        article_dict['source'] = source
        article_dict['author'] = author
        article_dict['title'] = title
        article_dict['description'] = desc
        article_dict['url'] = article_url
        article_dict['urlToImage'] = image_url
        article_dict['publishedAt'] = clean_bloomberg_date(date)
        article_dict['content'] = article_text

        output_list.append(article_dict)

    with open(out_path + '_'.join(query.split()) + '_' + str(len(output_list)) + '_Bloomberg_articles.json',
              'w') as json_file:
        json.dump(output_list, json_file)

    print(f"The scraping for {query} is done. There are {len(output_list)} articles.")
    return output_list


# execute function with unit tests
# Modify parameters here
out_path = "../data/unannotated_data/bloomberg/"
# Modify parameters here
bloomberg_mr_article = bnn_article_scraper('mortgage rates', out_path)
assert len(bloomberg_mr_article) == 100
assert os.path.exists(out_path + 'mortgage_rates_100_Bloomberg_articles.json')

bloomberg_ir_article = bnn_article_scraper('interest rates', out_path)
assert len(bloomberg_ir_article) == 100
assert os.path.exists(out_path + 'interest_rates_100_Bloomberg_articles.json')

bloomberg_hp_article = bnn_article_scraper('housing price', out_path)
assert len(bloomberg_hp_article) == 100
assert os.path.exists(out_path + 'housing_price_100_Bloomberg_articles.json')

bloomberg_e_article = bnn_article_scraper('employment', out_path)
assert len(bloomberg_e_article) == 100
assert os.path.exists(out_path + 'employment_100_Bloomberg_articles.json')

bloomberg_gdp_article = bnn_article_scraper('GDP', out_path)
assert len(bloomberg_gdp_article) == 100
assert os.path.exists(out_path + 'GDP_100_Bloomberg_articles.json')

bloomberg_tsx_article = bnn_article_scraper('stock market', out_path)
assert len(bloomberg_tsx_article) == 100
assert os.path.exists(out_path + 'stock_market_100_Bloomberg_articles.json')
