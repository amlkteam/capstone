# better_dwelling_capstone

#### Authors:

- Pandramishi Naga Sirisha
- Jonathan TK Chan
- Aaron Tian
- Amy Lam

 ---

### Capstone project reproduction instructions:

#### Last Updated On:

27 Jun 10:31pm added note on custom weights for new sources

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
- `total_count` (Integer) : The total number of articles to scrape


Example:

```
[DEFAULT]
economic_indicator="interest rates"
start_date="2019-01-01 00:00:00"
end_date="2020-05-01 00:00:00"
project_path="/Users/nagasiri/Desktop/NagaSiri/MDS-CL/Capstone/better_dwelling_capstone/"
total_count = 100
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
```

**Output :**

The following files are created:

Folder :

`../data/unannotated_data/bloomberg/extraction_first200pages_FP_BloombergNews`

File(s):

six `<economic_indicator_output.json>`

example: `interest_rate_output.json`


Dry run example:

```
cd data_extraction\src
python scrape_articles_FinancialPost.py
```

**3. Bloomberg News From BNN Bloomberg article scraping**

**Purpose:** To extract the articles from official website of [BNN Bloomberg](https://www.bnnbloomberg.ca/) execute the following script

Required files:

- `scrape_articles_bloomberg.py`

**Script name:** `scrape_articles_bloomberg.py`

**Input (parameters):** 

  - `query`, which represents the searching query
  - `out_path`, which represents the output file path
  - **By running the script, six pre-defined searching queries will be used to search articles from BNN Bloomberg website. (They are 'mortgage rates', 'interest rates', 'housing price', 'employment', 'GDP', and 'stock market') To use new queries and output path, please go to line 129 and line 131 of script `scrape_articles_bloomberg.py` and update the parameters. Line 135 to line 153 could be commented out if only one query is provided.**


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

 6 X `<ECONOMIC_INDICATOR_NUMBER_OF_ARTICLES_Bloomberg_article.json>`

example: `mortgage_rates_100_Bloomberg_article.json`


Dry run example:

```
cd data_extraction\src
python scrape_articles_bloomberg.py
```

notice: <ins>*Free users of BNN Bloomberg will only have access to 100 articles per query. Running the above script will scrape at most 100 latest articles from their website for each query.*</ins>

**4. CBC Sampling for annotation**

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


**5. Bloomberg Sampling for annotation**

**Purpose:** Sample the data from the Bloomberg articles that are extracted. The dataset to be used for annotation will be generated, the rest of the articles will be used for prediction. The data files used for annotation will be generate at `../data/annotated_data/bloomberg/`. And the data files for prediction will be generated at `../../sentiment_analyzer/data/predictions_data/bloomberg/`. <ins>*This step is optional if annotated data is already available. Sampling and annotation is for the fine-tuning phase of the algorithm.*</ins>

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

**1. Finetuning Sentiment Analyzer for a specific economic indicator**

**Purpose:** To execute two-stage finetuning on the pretrained general sentiment classifier, with first stage feeding in a general Financial News dataset (combined and balanced from 4000+ examples from [Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014)](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news), and 500 + examples from [Matheus Gomes de Sousa et. al](https://drive.google.com/file/d/1eqNwkqb1tnaJm_l975K6LJBic8pMof1x/view)), and second stage feeding in Canadian specific financial news datasets that we have labelled (~600 examples).

**Oversampling and undersampling:** Oversampling and undersampling are techniques used to adjust the class distribution of a dataset. We conducted oversampling by randomly sampling the under-represented classes with replacement and undersampling by randomly sampling the over-represented classes. For our experiment, we used the undersampling method for the datasets of employment and stock market, and implemented the oversampling method for the datasets of the rest four economic indicators.

Required files:

- `Two_stage_flair_training.py`
- `data_folder`, which contains the file "combined_benchmark.csv"
- `oversampled_data_folder or undersampled_data_folder`, which contains 6 subfolders, one for each economic indicator. Each subfolder contains 3 files: train.csv, dev.csv, test.csv.

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
    
both benchmark_classifier_folder and finetuned_classifier_folder will create the following files: best_model.pt, final_model.pt, loss.tsv, training.log and weights.txt. best_model.pt (or final_model.pt if it performs better on new data prediction) is necessary for  visualization module, other files could be discarded.  
    
Dry run example:
```
cd sentiment_analyzer/src
python Two_stage_flair_training.py
```
**2. Make predictions on news articles you want to check sentiment on**

**Purpose:** Make predictions on news articles based on title and subtitles

**Script name:** `Load_and_predict.py`

Required files:

- `Load_and_predict.py`
- data to be predicted on
- trained classifiers
- file location where predicted data will go

**Input (parameters/files, please go to line 73 to line 75 to edit):**
- `input_file_path`, file path of data to be predicted on, for example: '../data/predictions_data/bloomberg_or_cbc/FILE_NAME'
- `output_file_path`, file path of predicted data, for example: '../data/prediction_output/OUT_FILE_NAME'
- `classifier`, classifier that will be used to classify articles, for example:  TextClassifier.load('../trained_models/MODEL_NAME')

**Output :**

The predicted files will be stored in the prediction_output folder. Each prediction value includes the confidence scores for all three classes (positive, neutral, and negative). We need these three values to compute the final sentiment score for each article. The sentiment scores will be in a continuous scale.  

example:
```
cd sentiment_analyzer/src
python Load_and_predict.py
```

**3. Calculate final sentiment values**

**Purpose:** Calculate the final sentiment score for all the predicted data points, and combine them with annotated data point to a csv file, that will function as the input for visualization

**Script name:** `generate_senti_df.py`

Required files:

- `generate_senti_df.py`
- the file path where the annotated datasets are stored
- the file path where the predicted datasets are stored
- the file path where the output csv file will be located

**Input (parameters/files, please go to line 132 to line 134 to edit):**
- `annotation_path`, annotated datasets file path, for example: '../../data_extraction/data/annotated_data/combined/'
- `prediction_path`, predicted datasets file path, for example:  '../data/prediction_output/'
- `output_path`, output file path, for example: '../data/prediction_combined/'


**Output :**

A .csv file (`combined_sentiment_data.csv`) will be created in the prediction_combined folder. The file includes all the annotated and predicted data points. This file will directly function as an input for the visualization module. 

example:
```
cd sentiment_analyzer/src
python generate_senti_df.py
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

Note: user can change custom weights for each news source at line 382 in dash_frontend_final.py, to render Source-Weighted Average monthly and daily datapoints. Current placeholder weights are: {'Bloomberg': 0.7, 'CBC': 0.3}. 

**Output :**
- a Dash app running on local server

Dry run Example:
```
cd visualization/src
python dash_frontend_final.py
```

![Dash visualization app interface](https://github.ubc.ca/ltian05/better_dwelling_capstone/blob/master/readme_img/switch_indicator_graphs.gif)
