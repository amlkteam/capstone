#!/usr/bin/env python
# coding: utf-8




### CBC SCRAPING CODE
### Authors: PANDRAMISHI NAGA SIRISHA
### This script contains code to extract the articles from CBC news site
###MOST RECENT UPDATE:  
##2020 June 21, 11:52AM
#added documentation as per the code review
#extract_json_items() will run for all articles, and will return null if not in proper format

##2020 June 10 by Pandramishi Naga Sirisha, to write test cases, convert to .py file




import configparser
import urllib.request
import utility_main
import json 
from bs4 import BeautifulSoup
#from datetime import date
import requests
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta
import datetime
import pytz
import dateutil.parser
import os
from dateutil.parser import parse


#https://www.cbc.ca/search_api/v1/search?q=mortgage%20rate&sortOrder=relevance&page=100&fields=feed
def get_initial_url(search_term):
    """This function returns the URL of the first page API call of the CBC news website given a search string
    Input:
    ------ 
    search_term - string : The search string for retrieving articles
    
    Output:
    ------ 
    string - API call string 
    
    Example: first_url = get_initial_url("interest rates")
    """
    
    words = search_term.split()
    url_prefix = "https://www.cbc.ca/search_api/v1/search?"
    query = "q=" + "%20".join(words)
    url_suffix = "&sortOrder=relevance&page=1&fields=feed"
    first_url = url_prefix + query + url_suffix
    print("FIRST URL API CALL: ", first_url)
    return first_url
    

def scrape_urls(url, start_date, end_date):
    """This function takes in the first query url and scrapes all other articles from past 1 year and returns 
    the urls of such articles
    
    Input:
    ------
    url - string : The url of the first page
    start_date - date (format:''%Y-%m-%d %H:%M:%S') : The start date from which you want to retrieve articles from
    end_date - date (format:''%Y-%m-%d %H:%M:%S') : The start date from which you want to retrieve articles till
    
    Note: The default time zone will be taken as UTC 
    
    Example:
    # all_urls = scrape_urls(first_url, "2019-01-01 00:00:00", "2020-05-01 00:00:00")
    """
    count = 0
    url_list = []
    main_url = url
    r = requests.get(url)
    info = r.json()
    last_retrieved_items_count= len(info)
    
    timezone = pytz.timezone('UTC')
    start_date_string = parse(start_date)
    end_date_string = parse(end_date)
    start_tz_obj =  timezone.localize(start_date_string)
    end_tz_obj = timezone.localize(end_date_string)
    
    if start_tz_obj > end_tz_obj:
        print("The start date is more recent than end date, exiting... ")
        return None
    
    for i in info:
        
        if 'publishtime' in i.keys() and dateutil.parser.parse(i['publishtime']).astimezone(pytz.UTC) > start_tz_obj and dateutil.parser.parse(i['publishtime']) < end_tz_obj:   
            url_list.append(i['url'])
            count += 1
        
    page_number = 2
    
    while last_retrieved_items_count > 0 :
    # For retreiving specific amount of articles (ex: 100) set count < 100 
    #in the while block below and comment the line above
    #   while count < 10 :
        split_url = main_url.split('page')
        new_url = split_url[0] + "page=" + str(page_number) + "&fields=feed" 
        try:
            r = requests.get(new_url)
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)    
            return None
        
        info = r.json()
        last_retrieved_items_count= len(info)
        
        for i in info:
            if  'publishtime' in i.keys() and dateutil.parser.parse(i['publishtime']).astimezone(pytz.UTC) > start_tz_obj and dateutil.parser.parse(i['publishtime']) < end_tz_obj:
                url_list.append(i['url'])
                count += 1
                
        page_number += 1   
        print("page_number: ", page_number)

        
    print("The number of articles retrieved is: ", len(url_list))
    return url_list




def get_author(soup):
    """returns the author of a BeautifulSoup article if it exists, None if cannot be found
    
    Assume author info is contained within span tag (class: authorText)
    """
    author_span = soup.find("span", {"class": "authorText"})
    
    if author_span:
        return author_span.text
    else:
        #print("No author found in article!")
        return None



def get_desc(soup):
    """returns the description of a BeautifulSoup article if it exists, None if not
    
    Assume description is contained within h2 tag (class: deck)
    """
    desc_tag = soup.find("h2", {"class": "deck"})
    
    if desc_tag:
        desc_text = desc_tag.text
        return desc_text
    else:
        #print("No description found in article!")
        return None



def get_title(soup):
    """returns the title of a BeautifulSoup article if it exists, None if cannot be found
    
    Assume title info is contained within h1 tag (class: detailHeadline)
    """
    title_tag = soup.find("h1", {"class": "detailHeadline"})
    
    if title_tag:
        title_text = title_tag.text
        return title_text
    else:
        #print("no title found in article!")
        return None


def get_url_to_image(soup):
    """returns the url to the header image of a CBC article (BeautifulSoup) if it exists, None if not
    
    Assume image url is contained within src attribute of img tag 
    """
    main_image_tag = soup.find("figure", {"class": "imageMedia leadmedia-story full"})
    
    if main_image_tag:
        main_image_url = main_image_tag.find("img").attrs["src"]
        return main_image_url
    else:
        #print("No main header image found in article!")
        return None
        


def get_publish_time(soup):
    """returns a tuple of publish time string and datetime string if found in article, None if not
    
    Assume time is contained within time tag (class: timestamp)
    """
    time_tag = soup.find("time", {"class": "timeStamp"})
    if time_tag:
        datetime_str = time_tag.attrs["datetime"]
        
        #NOTE: if we want to return a datetime object, error when writing to JSON
        #datetime_obj = parser.isoparse(datetime_str)
        #SOLUTION: return as string for now, convert to datetime object later in pipeline
        
        #format of time_tag.text: 
        timetext_str = time_tag.text.split("|")[0].replace("Posted: ", "").strip()
        return (timetext_str, datetime_str)
    else:
        #print("No time information found in article!")
        return None




def get_source(soup, specify_source_type=True):
    """Returns the source of the article if it exists
    if specify_source_type, subdivision of CBC will be returned
    if not, "CBC" will be returned as the source
    
    
    Assume that source always starts with "CBC" (Ex: "CBC news", "CBC radio")
    Assume that source comes before span tag (class: bullet)
    """
    
    #source appears before <span class="bullet"> · </span>
    #if author is attached, there are two bullet tags
    #if no author attached, there is one bullet tag
    source = None
    
    if specify_source_type:
        bullet_spans = soup.find_all("span", {"class": "bullet"})
        for bullet_span in bullet_spans:
            previous_str = str(bullet_span.previous_sibling)
            if previous_str.startswith("CBC"):
                source = previous_str
    else:
        
        source = "CBC"
    
    if source:
        return source
    else:
        return None
    



def get_content(soup, as_string=True):
    """Returns the text content from a CBC article (as BeautifulSoup object)
    if as_string is True, return content as one string,
    if as_string is False, return content as list of paragraph strings
    
    Input: BeautifulSoup object, boolean
    
    """
    
    story_tag = soup.find("div", {"class": "story"}) 
    content_list = []
    
    if story_tag:
        for p_tag in story_tag.find_all("p"):
            p_text = p_tag.text + "\n"
            content_list.append(p_text)

        if as_string:
            final_content = "".join(content_list)
        else:
            final_content = content_list #return content as list of paragraph strings

        return final_content
    else:
        #print("no content found in article!")
        return None
    

def extract_json_items(url, specify_source_type=True):
    """Returns a json containing the following items from a CBC article:
        url: the url of the article
        urlToImage: the url of the header image
        title: the title of the article 
        description: subheader of the article
        author: author (note that some articles do not specify author)
        source: CBC if specify_source_type == False, subdivision of CBC if True (ex: "CBC radio")
        publishedAt: tuple of (date_string, datetime object)
        
        input: url returned from CBC API in "url" field (missing "http:" as part of URL)
        
    Example:
    extract_json_items('//www.cbc.ca/news/business/powel-trump-negative-rates-1.5567512')
    """
    json_dict = {}
    article_url = "http:" + url
    
    #get HTML from article URL into BeautifulSoup
    try:
        html_bytes = urllib.request.urlopen(article_url)
  
    except HTTPError as e:
        print('Error code: ', e.code)
        return None
    except URLError as e:
        print('Reason: ', e.reason)
        return None
    except:
        print("gone wrong")
        return None

    else:    
        mybytes = html_bytes.read()
        html = mybytes.decode("utf8")
        html_bytes.close()
        soup = BeautifulSoup(html, 'html.parser')
        author_name = get_author(soup)
        title_text = get_title(soup)
        desc_text = get_desc(soup)
        image_url = get_url_to_image(soup)
        publish_time = get_publish_time(soup)
        news_source = get_source(soup)
        content = get_content(soup, True)
        
        json_dict["author"] = author_name
        json_dict["title"] = title_text 
        json_dict["description"] = desc_text
        json_dict["url"] = article_url
        json_dict["urlToImage"] = image_url
        json_dict["publishedAt"] = publish_time
        json_dict["source"] = news_source
        json_dict["content"] = content
        final_json = json.dumps(json_dict)
       
        return json_dict



def main(query,start_date, end_date, project_path):
    """
    This function takes a search string, the start date and end_date to retrieve the articles
    from CBC website and stores articles retreived in a json file
    
    Input:
    ------
    url - string : The search term without special characters
    start_date - date (format:''%Y-%m-%d %H:%M:%S') : The start date from which you want to retrieve articles from
    end_date - date (format:''%Y-%m-%d %H:%M:%S') : The start date from which you want to retrieve articles till
    
    Note: The default time zone will be taken as UTC 
    
    Output:
    -------
    list of dictionaries of retrieved articles
    
    """
    directory_flag = utility_main.check_dir_exists(project_path)
    
    if  directory_flag == True:
        # path exists
        first_url = get_initial_url(query)
        all_urls = scrape_urls(first_url, start_date, end_date)
        json_list = []
    
        try:
            for each_url in all_urls:
                retrieved_json  = extract_json_items(each_url)
                
                if retrieved_json is not None:
                    print(each_url)
                    json_list.append(retrieved_json)

            full_query = query.split(" ")
            file_name_prefix = "".join(full_query)
            file_name = project_path + "project/data_extraction/data/unannotated_data/cbc/" + file_name_prefix + '_' +'CBC_article' + '.json' 
            
            with open( file_name, 'w') as json_file:
                json.dump(json_list, json_file)
            if utility_main.file_exists(file_name):
                print("The retrieved articles are written to the folder: ",file_name)
            else:
                print("Output file not created successfully")
            
        except:
            print("We could not match the selected criteria to extract articles, exiting...")
            return None
        
    elif directory_flag is False:
        print("directory_flag is False")
        print("Project path does not exist,exiting...")
        return None
        
    
    return json_list




config_file = input("Please enter the path to the config file: ")
# Example './twitter_config.ini'
# Example format of the config file
# [DEFAULT]
# economic_indicator="interest rates"
# start_date="2019-01-01 00:00:00"
# end_date="2020-05-01 00:00:00"
# project_path="/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
print(config_file)


# Initialize configparser object and read config file
config = configparser.ConfigParser()

try:
    config.read(config_file)
except:
    print("Config file cannot be read, please check the path")
    
# Read the configurations
economic_indicator = config.get('DEFAULT','economic_indicator').replace('"', '')
start_date = config.get('DEFAULT','start_date').replace('"', '')
end_date = config.get('DEFAULT','end_date').replace('"', '')
project_path = config.get('DEFAULT','project_path').replace('"', '')
print("The economic indicator is ", economic_indicator)
print("The start date is ", start_date)
print("The end date is ", end_date)
print("The project path is ", project_path)

main(economic_indicator,start_date,end_date,(project_path))


# ### For other economic indicators
# #### For interest rates,  the search string used is "interest rates"
# #### For housing price, the search used is   'housing price'
# #### For employment, the  search string used is "employment"
# #### For GDP,  the search string used is "gdp"
# #### For TSX, the search string used is "tsx", "stock market"

# In[34]:


def run_tests():
    first_url = get_initial_url("interest rates")
    project_path="/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/project/"
    
    # Check start date is earlier than end date
    x = main("interest rates", "2019-02-01 00:00:00", "2019-01-01 00:00:00", project_path)
    assert x is None, "if start date is greater than end date, None should be returned"
    
    # Check the "project" path exists
    project_path="/non_existenet_path"
    x = main("interest rates", "2019-01-01 00:00:00", "2019-02-01 00:00:00", project_path)
    assert x is None, "if project directory path does not exist, None should be returned"

run_tests()

