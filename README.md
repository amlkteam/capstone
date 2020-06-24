# better_dwelling_capstone

#### Authors:

- Pandramishi Naga Sirisha
- Jonathan TK Chan
- Aaron Tian
- Amy Lam

 ---

### Capstone project reproduction instructions:

#### Last Updated On:

24 Jun 1:13pm added note on neccessary versions

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
**Flair**| **0.5** |
requests | 2.23.0 |
beautifulsoup4 | 4.9.1 |
pandas | 1.0.2 |
scikit_learn | 0.23.1 |
scipy | 1.4.1 |
dash | 1.10.0 |
plotly | 4.5.4  |
dash_core_components  | 1.9.0  |
dash_html_components  | 1.0.3  |

Note: bolded dependency must be the specified version; unbolded ones represent the versions we used and tested.

---------------------------------------------------------------------------------------------------------------------------
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

example: `interestrates_CBC_article.json`


Dry run example:

`python scrape_articles_cbc.py`

>Enter the path to the config file:
`./cbc_scraping_config.ini`

**2. Bloomberg News From Financial Post article scraping**

**Purpose:** To extract the articles from author "Bloomberg News" on Financial Post website execute the following script

Required files:

- `scrape_articles_FinancialPost.py`

**Script name:** `scrape_articles_FinancialPost.py`

**Input (parameters/files):** 

 - `output_folder`
 - `end number of pages to extract`
 
Example:
```
output_folder = '../data/unannotated_data/bloomberg/extraction_first200pages_FP_BloombergNews'
end_page = 200
BloombergNews_from_FP(end_page,output_folder)   
separate_into_indicator_baskets(output_folder)
```

**Output :**

The following files are created:

Folder :

`../data/unannotated_data/bloomberg/extraction_first200pages_FP_BloombergNews`

File(s):

 `<economic_indicator_output.json>`

example: `interest_rate_output.json`


Dry run example:

```
cd data_extraction\src
python scrape_articles_FinancialPost.py
```

**3. Bloomberg News From BNN Bloomberg article scraping**

**Purpose:** To extract the articles from author "Bloomberg News" on BNN Bloomberg website execute the following script

Required files:

- `scrape_articles_bloomberg.py`

**Script name:** `scrape_articles_bloomberg.py`

**Input (parameters):** 

  - `query`, which represents the searching query
  - `out_path`, which represents the output file path


Example:
```
query = 'mortgage rates'
outpath = '../data/unannotated_data/bloomberg/'

```

**Output :**

The following files are created:

Folder :

`../data/unannotated_data/bloomberg/`

File(s):

 `<ECONOMIC_INDICATOR_NUMBER_OF_ARTICLES_Bloomberg_article.json>`

example: `mortgage_rates_100_Bloomberg_article.json`


Dry run example:

```
cd data_extraction\src
python scrape_articles_bloomberg.py
```

notice: Running the above script will scrape the latest 100 articles from BNN Bloomberg website for each searching query. 

**4. CBC Sampling**

**Purpose:** To sample the data from the CBC articles that are extracted to be split into data to_annotate and data to_predict

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
`../sentiment_analyzer/data/predictions_data/cbc/<predictions_dataset_economicindicator_cbc.csv>`

Example:

`../data_extraction/data/annotated_data/cbc/interestrates_sample.csv`
`../sentiment_analyzer/data/predictions_data/cbc/predictions_dataset_interestrates_cbc.csv`

Dry run example:

`python sample_articles_cbc.py`


**5. Bloomberg Sampling**

**Purpose:** Sample the data from the Bloomberg articles that are extracted from annotation and prediction. The dataset that will be used for annotation and prediction will be generated, the rest of the articles will be used for prediction. The data files used for annotation will be generate at `../data/annotated_data/bloomberg/`. And the data files for prediction will be generated at `../../sentiment_analyzer/data/predictions_data/bloomberg/` 

Required files:

- `sample_and_combine.py`



**Script name:** `sample_and_combine.py`




**Output :**

The following files are created:



File(s):
 `../data/annotated_data/bloomberg/KEYWORD_combined_sampled.csv`
 
 `../sentiment_analyzer/data/predictions_data/bloomberg/<predictions_dataset_economicindicator_cbc.csv>`

Example:

`../data/annotated_data/bloomberg/Bloomberg_interestrates_combined_sampled.csv`

`../sentiment_analyzer/data/predictions_data/bloomberg/predictions_dataset_interestrates_Bloomberg.csv`

Dry run example:

`python sample_and_combine.py`

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
- indicators_df_path: the csv file that contains all the indicators values.
- senti_df_path: The csv file containing aggregated sentiment data of both annotated and predicted data under each indicator and each source.

**Output :**
- a Dash app running on local server

Dry run Example:
```
cd visualization/src
python dash_frontend_final.py
```
