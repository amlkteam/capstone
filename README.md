# better_dwelling_capstone

## Week 1 : 
Final submission:

https://github.ubc.ca/ltian05/better_dwelling_capstone/blob/master/week_1/Better%20Dwelling%20Capstone%20Week1%20Project%20Plan.pdf

https://github.ubc.ca/ltian05/better_dwelling_capstone/blob/master/week_1/Teamwork%20Contract.pdf


 ---
title: "README"
author: "Naga Sirisha"
date: "20/06/2020"
output: github_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```



#### Authors:

- Pandramishi Naga Sirisha
- Jonathan TK Chan
- Aaron Tian
- Amy Lam

#### Last Updated On:

20 Jun, added instructions for `scrape_articles_cbc.py`

#### <u> Initial project structure </u>

The git repo is to be cloned into a folder in the local directory of the user.

**Project path:** This is the absolute path to the project folder

Example: C:/Users/Documents/better_dwelling

**Project structure:**

The directory `C:/Users/Documents/better_dwelling/` will contain the following structure

```
better_dwelling
  - /data_extraction
  - /sentiment_analyzer
  - /visualization
```

**Dependency Packages and Libraries:**

|Package| Version|
------:|-------:|
Python| 3.2|
Flair| |

### <u>Data Extraction Module:</u>

**1. CBC  article scraping**

**Purpose:** To extract the data from the CBC news site execute the following script

Required files:

- `scrape_articles_cbc.py`
- `utilities_main.py`
- `cbc_scraping_config.ini`

**Script name:** `scrape_articles_cbc.py`

**Input (parameters/files):** `cbc_scraping_config.ini`

This file contains the following format

- `economic_indicator`(String) : The economic indicator to be searched for in the CBC website. This term will be used as the search term to query the CBC API.
- `start_date` (String - yyyy/mm/dd hh:mm:s) : The start date from which you want to scrape the articles.
- `end_date`(String - yyyy/mm/dd hh:mm:s) : The end date until which you want to scrape the articles
- `project_path` (String): The path to the project folder

Example:

```
[DEFAULT]
economic_indicator="interest rates"
start_date="2019-01-01 00:00:00"
end_date="2020-05-01 00:00:00"
project_path="/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
```


**Output :**

The following files are created:

Folder :

`../data_extraction/data/unannotated_data/cbc/`

File(s):

 `<economic_indicator_CBC_article.json>`

ex: `interestrates_CBC_article.json>`


Dry run example:

`python scrape_articles_cbc.py`

>Enter the path to the config file:
`./cbc_scraping_config.ini`



**2. CBC Sampling**

**Purpose:** To sample the data from the CBC articles that are extracted  to be split into data to_annotate and data to_predict

Required files:

- `sample_articles_cbc.py`
- `utilities_main.py`


**Script name:** `sample_articles_cbc.py`

**Input (parameters/files):** 

None


**Output :**

The following files are created:



File(s):

 `../data_extraction/data/annotated_data/cbc/<economic_indicator_sample.json>`
`../sentiment_analyzer/data/predictions_data/cbc/<predictions_dataset_economicindicator_cbc.csv`

Example:

`../data_extraction/data/annotated_data/cbc/interestrates_sample.csv`
`../sentiment_analyzer/data/predictions_data/cbc/predictions_dataset_interestrates_cbc.csv`

Dry run example:

`python sample_articles_cbc.py`





