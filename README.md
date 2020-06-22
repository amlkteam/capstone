# better_dwelling_capstone

#### Authors:

- Pandramishi Naga Sirisha
- Jonathan TK Chan
- Aaron Tian
- Amy Lam

## Week 1 : 
Final submission:

https://github.ubc.ca/ltian05/better_dwelling_capstone/blob/master/week_1/Better%20Dwelling%20Capstone%20Week1%20Project%20Plan.pdf

https://github.ubc.ca/ltian05/better_dwelling_capstone/blob/master/week_1/Teamwork%20Contract.pdf


 ---

Capstone project reproduction readme:

#### Last Updated On:

22 Jun

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
Python| 3.7|
Flair| 0.5 |
requests | 2.23.0 |
beautifulsoup4 | 4.9.1 |
pandas | 1.0.2 |
scikit_learn | 0.23.1 |
scipy | 1.4.1 |
dash | 1.10.0 |
plotly | 4.5.4  |
dash_core_components  | 1.9.0  |
dash_html_components  | 1.0.3  |

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

-----------------------------------------------------------------------------------------------------------------------------

### <u>Sentiment Analyzer Module:</u>

**Purpose:** To execute two-stage finetuning on the pretrained general sentiment classifier, with first stage feeding in a general Financial News dataset (4000+ examples from [Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014)](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news) ), and second stage feeding in Canadian specific financial news datasets that we have labelled (~600 examples).

Required files:

- `Two_stage_flair_training.py`
- `data_folder`, which contains the file "combined_benchmark.csv"
- `oversampled_data_folder or undersampled_data_folder`, which contains 6 subfolders for each economic indicator. Each subfolder contains 3 files: train.csv, dev.csv, test.csv.

**Script name:** `Two_stage_flair_training.py`

**Input (parameters/files):** 

    # data_folder contains the file "combined_benchmark.csv" that will be used in first-stage training
    data_folder = r"../data/annotated_sample_for_training//"

    # benchmark_classifier_folder is where the first-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    benchmark_classifier_folder = r'../trained_models/gdp_benchmark_classifier//'

    # load a subfolder for second-stage training: for example, loading in articles related to GDP
    new_data_folder = r'../data/oversampled_training_data_combined/GDP//'

    # finetuned_classifier_folder is where the second-stage trainer will save best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    finetuned_classifier_folder = r'../trained_models/gdp_finetuned_classifier//'

**Output :**
    
both benchmark_classifier_folder and finetuned_classifier_folder will create the following files: best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt
    
Dry run example:
```
cd sentiment_analyzer/src
python Two_stage_flair_training.py
```

-----------------------------------------------------------------------------------------------------------------------

### <u>Visualization Module:</u>

**Purpose:** To visualize the correlation between changes in news sentiment against trend in economic indicator over a period of time.

Required files:
- `../data/combined_indicator_data.csv`
- `../data/combined_sentiment_data.csv`
- `dash_frontend_final.py`


**Script name:** `dash_frontend_final.py`

**Input (parameters/files):** 
- indicators_df_path
- senti_df_path

**Output :**
- a Dash app running on local server

Dry run Example:
```
cd visualization/src
python dash_frontend_final.py
```
